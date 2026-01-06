import asyncio
from typing import Dict


class LockManager:
    """
    Manages asyncio locks per SKU to ensure
    concurrency-safe inventory operations.
    """

    def __init__(self):
        self._locks: Dict[str, asyncio.Lock] = {}

    def get_lock(self, sku: str) -> asyncio.Lock:
        """
        Returns a lock for the given SKU.
        Creates one if it does not exist.
        """
        if sku not in self._locks:
            self._locks[sku] = asyncio.Lock()
        return self._locks[sku]
