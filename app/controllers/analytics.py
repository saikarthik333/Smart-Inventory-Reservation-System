from fastapi import APIRouter
from app.services.health_service import HealthService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

health_service = HealthService()


@router.get("/inventory/{sku}")
async def inventory_health(sku: str):
    """
    Returns inventory demand & health metrics for a SKU.
    """
    return health_service.get_inventory_health(sku)
