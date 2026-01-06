from app.storage import store


class WaitlistService:
    """
    Manages FIFO waitlists and auto-upgrades reservations
    when inventory becomes available.
    """

    def __init__(self, reservation_service):
        """
        reservation_service is injected to avoid circular imports.
        """
        self.reservation_service = reservation_service

    async def add_to_waitlist(self, sku: str, user_id: str, quantity: int):
        """
        Add a user request to the SKU waitlist (FIFO).
        """
        store.add_to_waitlist(
            sku,
            {
                "sku": sku,
                "user_id": user_id,
                "quantity": quantity
            }
        )

    async def try_upgrade_waitlist(self, sku: str):
        """
        Try to convert the first waitlisted request into
        an active reservation.
        """
        next_request = store.pop_from_waitlist(sku)

        if not next_request:
            return None

        try:
            # Attempt to create reservation for waitlisted user
            return await self.reservation_service.create_reservation(
                sku=next_request["sku"],
                user_id=next_request["user_id"],
                quantity=next_request["quantity"]
            )
        except Exception:
            # If it still fails, put the request back into waitlist
            store.add_to_waitlist(sku, next_request)
            return None
