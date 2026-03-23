from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrdersWatchesBase(BaseModel):
    order_id: int
    watch_id: int


class OrdersWatchesCreate(OrdersWatchesBase):
    pass


class OrdersWatchesUpdate(BaseModel):
    order_id: Optional[int] = None
    watch_id: Optional[int] = None


class OrdersWatchesInfo(BaseModel):
    id: int
    order_id: int
    watch_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
