from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_session
from app.schemas.cart import CartItem, CartItemCreate
from app.services.cart_service import CartService
from app.core.security import get_current_user
from app.models.users import User

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/", response_model=CartItem, summary='Add item to cart', description="Add a specified quantity of a menu item to the user's cart.")
async def add_to_cart(
    item: CartItemCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await CartService.add_to_cart(db, current_user.id, item)

@router.get("/", response_model=List[CartItem], summary='Get cart items', description="Retrieve all items currently in the user's cart.")
async def get_cart(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await CartService.get_cart(db, current_user.id)

@router.delete("/{item_id}", status_code=204, summary='Remove item from cart', description="Remove an item from the user's cart by its ID.")
async def remove_from_cart(
    item_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    await CartService.remove_from_cart(db, current_user.id, item_id)