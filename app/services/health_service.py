from app.storage import store


class HealthService:
    """
    Provides system-level inventory and demand metrics.
    """

    def get_inventory_health(self, sku: str):
        available = store.get_inventory(sku)
        waitlist_size = len(store.get_waitlist(sku))

        if available == 0 and waitlist_size > 0:
            status = "HIGH_DEMAND"
        elif available > 0:
            status = "HEALTHY"
        else:
            status = "OUT_OF_STOCK"

        return {
            "sku": sku,
            "available_inventory": available,
            "waitlist_size": waitlist_size,
            "status": status
        }
