from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int
    class Config:
        orm_mode = True