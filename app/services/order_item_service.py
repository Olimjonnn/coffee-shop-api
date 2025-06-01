from sqlalchemy.future import select
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.menu_item import MenuItem


class OrderItemService:
    @staticmethod
    async def create_order_from_cart(db: AsyncSession, user_id: str) -> Order:
        result = await db.execute(select(CartItem).where(CartItem.user_id == user_id))
        cart_items = result.scalars().all()

        if not cart_items:
            raise Exception("Cart is empty")

        total = 0
        order_items = []

        for ci in cart_items:
            menu_item = await db.get(MenuItem, ci.menu_item_id)
            if not menu_item:
                continue
            price = menu_item.price
            total += price * ci.quantity
            order_items.append(OrderItem(menu_item_id=ci.menu_item_id, quantity=ci.quantity, price=price))

        order = Order(user_id=user_id, total_amount=total)

        db.add(order)
        await db.flush()

        for oi in order_items:
            oi.order_id = order.id
            db.add(oi)

        for ci in cart_items:
            await db.delete(ci)

        await db.commit()
        await db.refresh(order)
        return order