from typing import Dict


class InMemoryStore:
    """
    Central in-memory data store.
    Acts like a lightweight Redis replacement.
    """

    def __init__(self):
        # sku -> available quantity
        self.inventory: Dict[str, int] = {}

    def set_inventory(self, sku: str, quantity: int):
        """Initialize or reset inventory for a SKU"""
        self.inventory[sku] = quantity

    def get_inventory(self, sku: str) -> int:
        """Get available inventory for a SKU"""
        return self.inventory.get(sku, 0)

    def decrement_inventory(self, sku: str, quantity: int):
        """Reduce inventory safely (caller must ensure availability)"""
        if sku not in self.inventory:
            raise ValueError("SKU does not exist")
        self.inventory[sku] -= quantity

    def increment_inventory(self, sku: str, quantity: int):
        """Increase inventory (used on cancel/expiry)"""
        if sku not in self.inventory:
            self.inventory[sku] = 0
        self.inventory[sku] += quantity
