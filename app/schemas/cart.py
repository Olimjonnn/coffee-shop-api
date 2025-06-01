from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    menu_item_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    user_id: str

    class Config:
        orm_mode = True