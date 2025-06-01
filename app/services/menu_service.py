from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.schemas.menu import CategoryCreate, MenuItemCreate


class MenuService:

    @staticmethod
    async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
        category = Category(**category_in.dict())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_categories(db: AsyncSession):
        result = await db.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def create_menu_item(db: AsyncSession, item_in: MenuItemCreate) -> MenuItem:
        item = MenuItem(**item_in.dict())
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def get_menu_items(db: AsyncSession):
        result = await db.execute(select(MenuItem))
        return result.scalars().all()