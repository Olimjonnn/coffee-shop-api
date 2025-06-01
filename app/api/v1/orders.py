from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.orders import Order, OrderCreate, OrderUpdate
from app.services.order_service import OrderService
from app.db.session import get_async_session
from app.core.security import get_current_user

from app.models.users import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    order_in.user_id = current_user.id
    return await OrderService.create_order(db, order_in)

@router.get("/{order_id}", response_model=Order)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    order = await OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return order

@router.get("/", response_model=List[Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return await OrderService.get_orders(db, skip=skip, limit=limit)
    return await OrderService.get_user_orders(db, user_id=current_user.id, skip=skip, limit=limit)

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    order = await OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    updated_order = await OrderService.update_order(db, order, order_in)
    return updated_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_async_session)):
    order = await OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await OrderService.delete_order(db, order)
    return None

