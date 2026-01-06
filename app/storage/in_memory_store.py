from typing import Dict


class InMemoryStore:
    """
    Central in-memory data store.
    Acts like a lightweight Redis replacement.
    """

    def __init__(self):
        # sku -> available quantity
        self.inventory: Dict[str, int] = {}

        # reservation_id -> reservation data
        self.reservations: Dict[str, dict] = {}

        # user_id -> stats
        self.user_stats: Dict[str, dict] = {}

    # ---------- Inventory ----------

    def set_inventory(self, sku: str, quantity: int):
        self.inventory[sku] = quantity

    def get_inventory(self, sku: str) -> int:
        return self.inventory.get(sku, 0)

    def decrement_inventory(self, sku: str, quantity: int):
        if sku not in self.inventory:
            raise ValueError("SKU does not exist")
        self.inventory[sku] -= quantity

    def increment_inventory(self, sku: str, quantity: int):
        if sku not in self.inventory:
            self.inventory[sku] = 0
        self.inventory[sku] += quantity

    # ---------- Reservations ----------

    def save_reservation(self, reservation_id: str, data: dict):
        self.reservations[reservation_id] = data

    def get_reservation(self, reservation_id: str):
        return self.reservations.get(reservation_id)

    def delete_reservation(self, reservation_id: str):
        if reservation_id in self.reservations:
            del self.reservations[reservation_id]

    def get_all_reservations(self):
        return self.reservations

    # ---------- User stats (Fairness) ----------

    def get_user_stats(self, user_id: str) -> dict:
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "total_reservations": 0,
                "successful_checkouts": 0
            }
        return self.user_stats[user_id]

    def record_reservation(self, user_id: str):
        stats = self.get_user_stats(user_id)
        stats["total_reservations"] += 1

    def record_successful_checkout(self, user_id: str):
        stats = self.get_user_stats(user_id)
        stats["successful_checkouts"] += 1
        
    # ---------- Waitlist ----------

    def add_to_waitlist(self, sku: str, data: dict):
        if sku not in self.waitlists:
            self.waitlists[sku] = []
        self.waitlists[sku].append(data)

    def pop_from_waitlist(self, sku: str):
        if sku in self.waitlists and self.waitlists[sku]:
            return self.waitlists[sku].pop(0)
        return None

    def get_waitlist(self, sku: str):
        return self.waitlists.get(sku, [])

