from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: str
    total_amount: float
    items: List[OrderItem]

    class Config:
        orm_mode = True