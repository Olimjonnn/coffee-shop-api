from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy import select


class OrderService:

    @staticmethod
    async def get_user_orders(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Order).where(Order.user_id == user_id).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
        order = Order(**order_in.dict())
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def get_order(db: AsyncSession, order_id: int) -> Order | None:
        return await db.get(Order, order_id)

    @staticmethod
    async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await db.execute(
            Order.__table__.select().offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_order(db: AsyncSession, order: Order, order_in: OrderUpdate) -> Order:
        for field, value in order_in.dict(exclude_unset=True).items():
            setattr(order, field, value)
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def delete_order(db: AsyncSession, order: Order) -> None:
        await db.delete(order)
        await db.commit()