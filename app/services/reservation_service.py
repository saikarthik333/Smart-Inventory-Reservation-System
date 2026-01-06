import uuid
from datetime import datetime, timedelta

from app.storage import store
from app.services.inventory_service import InventoryService
from app.services.fairness_service import FairnessService


class ReservationService:
    """
    Handles reservation lifecycle:
    create, confirm, cancel, expire
    """

    RESERVATION_TTL_SECONDS = 300  # 5 minutes

    def __init__(self):
        self.inventory_service = InventoryService()

    async def create_reservation(self, sku: str, user_id: str, quantity: int):
        """
        Idempotent reservation creation.
        If same user already has an active reservation for this SKU,
        return it instead of creating a new one.
        """

        # Idempotency check
        for reservation in store.get_all_reservations().values():
            if (
                reservation["sku"] == sku
                and reservation["user_id"] == user_id
                and reservation["status"] == "RESERVED"
            ):
                return reservation
        
        

        # Reserve inventory (this is concurrency-safe)
        
        # Record user attempt
        store.record_reservation(user_id)

        ttl_seconds = self.fairness_service.get_ttl_seconds(user_id)

        # Reserve inventory (concurrency-safe)
        await self.inventory_service.reserve_inventory(sku, quantity)

        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)


        reservation_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(seconds=self.RESERVATION_TTL_SECONDS)

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
        
        

        # Check expiry
        if reservation["expires_at"] < datetime.utcnow():
            await self.expire_reservation(reservation_id)
            raise ValueError("Reservation expired")

        reservation["status"] = "CONFIRMED"
        return reservation

    async def cancel_reservation(self, reservation_id: str):
        reservation = store.get_reservation(reservation_id)

        if not reservation:
            raise ValueError("Reservation not found")

        if reservation["status"] != "RESERVED":
            raise ValueError("Reservation cannot be cancelled")

        # Release inventory
        await self.inventory_service.release_inventory(
            reservation["sku"], reservation["quantity"]
        )

        reservation["status"] = "CANCELLED"
        return reservation

    async def expire_reservation(self, reservation_id: str):
        reservation = store.get_reservation(reservation_id)

        if not reservation or reservation["status"] != "RESERVED":
            return

        await self.inventory_service.release_inventory(
            reservation["sku"], reservation["quantity"]
        )

        reservation["status"] = "EXPIRED"
        
        store.record_successful_checkout(reservation["user_id"])

