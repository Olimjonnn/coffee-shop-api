from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart_item import CartItem
from app.schemas.cart import CartItemCreate

class CartService:

    @staticmethod
    async def add_to_cart(db: AsyncSession, user_id: str, item: CartItemCreate) -> CartItem:
        result = await db.execute(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.menu_item_id == item.menu_item_id)
        )
        cart_item = result.scalars().first()
        if cart_item:
            cart_item.quantity += item.quantity
        else:
            cart_item = CartItem(user_id=user_id, **item.dict())
            db.add(cart_item)

        await db.commit()
        await db.refresh(cart_item)
        return cart_item

    @staticmethod
    async def get_cart(db: AsyncSession, user_id: str):
        result = await db.execute(select(CartItem).where(CartItem.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def remove_from_cart(db: AsyncSession, user_id: str, item_id: int):
        result = await db.execute(
            select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
        )
        cart_item = result.scalars().first()
        if cart_item:
            await db.delete(cart_item)
            await db.commit()