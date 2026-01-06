from fastapi import APIRouter
from app.services.health_service import HealthService
from app.services.ai_insight_service import AIInsightService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

health_service = HealthService()
ai_service = AIInsightService()


@router.get("/inventory/{sku}")
async def inventory_health(sku: str):
    return health_service.get_inventory_health(sku)


@router.get("/ai/inventory/{sku}")
async def ai_inventory_insight(sku: str):
    return ai_service.generate_inventory_insight(sku)
