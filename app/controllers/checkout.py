from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.reservation_service import ReservationService

router = APIRouter(tags=["Checkout"])

reservation_service = ReservationService()


class ReserveRequest(BaseModel):
    sku: str
    user_id: str
    quantity: int


class ReservationActionRequest(BaseModel):
    reservation_id: str


@router.post("/inventory/reserve")
async def reserve_inventory(request: ReserveRequest):
    try:
        reservation = await reservation_service.create_reservation(
            sku=request.sku,
            user_id=request.user_id,
            quantity=request.quantity
        )
        return reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout/confirm")
async def confirm_checkout(request: ReservationActionRequest):
    try:
        reservation = await reservation_service.confirm_reservation(
            request.reservation_id
        )
        return reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout/cancel")
async def cancel_checkout(request: ReservationActionRequest):
    try:
        reservation = await reservation_service.cancel_reservation(
            request.reservation_id
        )
        return reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
