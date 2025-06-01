from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.menu import Category, CategoryCreate, MenuItem, MenuItemCreate
from app.services.menu_service import MenuService
from app.db.session import get_async_session
from app.core.security import get_current_user
from app.models.users import User

router = APIRouter(prefix='/menu', tags=["Menu"])


# Categories
@router.post('/categories/', response_model=Category, summary='Create a category', description='Create a new category in the menu.')
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await MenuService.create_category(db, category_in)


@router.get('/categories/', response_model=List[Category], summary='List categories', description='Retrieve a list of all categories in the menu.')
async def get_categories(
    db: AsyncSession = Depends(get_async_session)
):
    return await MenuService.get_categories(db)


# Menu Items
@router.post('/items/', response_model=MenuItem, summary='Create a menu item', description='Create a new menu item in the menu.')
async def create_menu_item(
    item_in: MenuItemCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await MenuService.create_menu_item(db, item_in)


@router.get('/items/', response_model=List[MenuItem], summary='List menu items', description='Retrieve a list of all menu items.')
async def get_menu_items(
    db: AsyncSession = Depends(get_async_session)
):
    return await MenuService.get_menu_items(db)