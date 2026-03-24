from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OrdersBase(BaseModel):
    user_id: int
    total_price: float = Field(gt=0)
    discount: Optional[int] = None
    is_pickup: bool = False
    delivery_address: Optional[str] = None
    notification_email: Optional[str] = None


class OrdersCreate(OrdersBase):
    pass


class OrdersUpdate(BaseModel):
    user_id: Optional[int] = None
    total_price: Optional[float] = None
    discount: Optional[int] = None
    is_pickup: Optional[bool] = None
    delivery_address: Optional[str] = None
    notification_email: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|confirmed|shipped|delivered|cancelled)$")


class OrdersInfo(BaseModel):
    id: int
    user_id: int
    total_price: float
    discount: Optional[int] = None
    is_pickup: bool
    delivery_address: Optional[str] = None
    notification_email: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
