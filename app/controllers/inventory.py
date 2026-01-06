from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

inventory_service = InventoryService()


class InventoryInitRequest(BaseModel):
    sku: str
    quantity: int


@router.post("/init")
async def init_inventory(request: InventoryInitRequest):
    try:
        await inventory_service.set_inventory(request.sku, request.quantity)
        return {
            "message": "Inventory initialized",
            "sku": request.sku,
            "quantity": request.quantity
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{sku}")
async def get_inventory(sku: str):
    quantity = await inventory_service.get_available_inventory(sku)
    return {
        "sku": sku,
        "available_quantity": quantity
    }
