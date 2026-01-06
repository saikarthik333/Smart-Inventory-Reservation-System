import uuid
from datetime import datetime, timedelta

from app.storage import store
from app.services.inventory_service import InventoryService
from app.services.fairness_service import FairnessService
from app.services.waitlist_service import WaitlistService


class ReservationService:
    """
    Handles reservation lifecycle:
    create, confirm, cancel, expire
    """

    def __init__(self):
        self.inventory_service = InventoryService()
        self.fairness_service = FairnessService()
        self.waitlist_service = WaitlistService(self)


    async def create_reservation(self, sku: str, user_id: str, quantity: int):
        """
        Idempotent reservation creation with fairness + waitlist.
        """

        # ---------- Idempotency ----------
        for reservation in store.get_all_reservations().values():
            if (
                reservation["sku"] == sku
                and reservation["user_id"] == user_id
                and reservation["status"] == "RESERVED"
            ):
                return reservation

        # ---------- Fairness ----------
        store.record_reservation(user_id)
        ttl_seconds = self.fairness_service.get_ttl_seconds(user_id)

        # ---------- Inventory reserve or waitlist ----------
        try:
            await self.inventory_service.reserve_inventory(sku, quantity)
        except ValueError:
            await self.waitlist_service.add_to_waitlist(sku, user_id, quantity)
            return {
                "status": "WAITLISTED",
                "sku": sku,
                "user_id": user_id
            }

        # ---------- Create reservation ----------
        reservation_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

        reservation = {
            "reservation_id": reservation_id,
            "sku": sku,
            "user_id": user_id,
            "quantity": quantity,
            "status": "RESERVED",
            "expires_at": expires_at
        }

        store.save_reservation(reservation_id, reservation)
        return reservation

    async def confirm_reservation(self, reservation_id: str):
        reservation = store.get_reservation(reservation_id)

        if not reservation:
            raise ValueError("Reservation not found")

        if reservation["status"] != "RESERVED":
            raise ValueError("Reservation cannot be confirmed")

        if reservation["expires_at"] < datetime.utcnow():
            await self.expire_reservation(reservation_id)
            raise ValueError("Reservation expired")

        reservation["status"] = "CONFIRMED"

        # ✅ success only on confirm
        store.record_successful_checkout(reservation["user_id"])

        return reservation

    async def cancel_reservation(self, reservation_id: str):
        reservation = store.get_reservation(reservation_id)

        if not reservation:
            raise ValueError("Reservation not found")

        if reservation["status"] != "RESERVED":
            raise ValueError("Reservation cannot be cancelled")

        await self.inventory_service.release_inventory(
            reservation["sku"], reservation["quantity"]
        )

        reservation["status"] = "CANCELLED"

        # auto-upgrade waitlist
        await self.waitlist_service.try_upgrade_waitlist(reservation["sku"])

        return reservation

    async def expire_reservation(self, reservation_id: str):
        reservation = store.get_reservation(reservation_id)

        if not reservation or reservation["status"] != "RESERVED":
            return

        await self.inventory_service.release_inventory(
            reservation["sku"], reservation["quantity"]
        )

        reservation["status"] = "EXPIRED"

        await self.waitlist_service.try_upgrade_waitlist(reservation["sku"])
