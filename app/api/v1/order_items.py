from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.services.order_item_service import OrderItemService
from app.db.session import get_async_session
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.orderitems import OrderRead

router = APIRouter(prefix='/order-items', tags=['order-items'])

@router.post('/from-cart', response_model=OrderRead, summary='Create order from cart', description="Create a new order using all items currently in the user's cart.")
async def create_order_from_cart(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    try:
        order = await OrderItemService.create_order_from_cart(db, current_user.id)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))