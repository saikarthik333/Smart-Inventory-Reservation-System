from app.storage import store
from app.utils import lock_manager


class InventoryService:
    """
    Business logic for inventory management.
    Ensures accuracy and concurrency safety.
    """

    async def get_available_inventory(self, sku: str) -> int:
        return store.get_inventory(sku)

    async def set_inventory(self, sku: str, quantity: int):
        if quantity < 0:
            raise ValueError("Inventory quantity cannot be negative")
        store.set_inventory(sku, quantity)

    async def reserve_inventory(self, sku: str, quantity: int):
        """
        Attempt to reserve inventory.
        This method is concurrency-safe and prevents overselling.
        """
        lock = lock_manager.get_lock(sku)

        async with lock:
            available = store.get_inventory(sku)

            if available < quantity:
                raise ValueError("Insufficient inventory")

            store.decrement_inventory(sku, quantity)

    async def release_inventory(self, sku: str, quantity: int):
        """
        Release inventory back (used on cancel / expiry).
        """
        lock = lock_manager.get_lock(sku)

        async with lock:
            store.increment_inventory(sku, quantity)
