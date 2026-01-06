from app.storage import store
from app.services.reservation_service import ReservationService


class WaitlistService:
    """
    Manages FIFO waitlists and auto-upgrades reservations.
    """

    def __init__(self):
        self.reservation_service = ReservationService()

    async def add_to_waitlist(self, sku: str, user_id: str, quantity: int):
        store.add_to_waitlist(sku, {
            "sku": sku,
            "user_id": user_id,
            "quantity": quantity
        })

    async def try_upgrade_waitlist(self, sku: str):
        """
        Attempt to convert the next waitlisted user into a reservation.
        """
        next_request = store.pop_from_waitlist(sku)

        if not next_request:
            return None

        try:
            reservation = await self.reservation_service.create_reservation(
                sku=next_request["sku"],
                user_id=next_request["user_id"],
                quantity=next_request["quantity"]
            )
            return reservation
        except Exception:
            # If reservation still fails, put back into waitlist
            store.add_to_waitlist(sku, next_request)
            return None
