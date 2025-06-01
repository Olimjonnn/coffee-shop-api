from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    status: Optional[str] = "pending"
    total_amount: Optional[float] = 0.0

class OrderCreate(OrderBase):
    user_id: Optional[int] = None

class OrderUpdate(BaseModel):
    status: Optional[str]
    total_amount: Optional[float]


class OrderInDBBase(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True