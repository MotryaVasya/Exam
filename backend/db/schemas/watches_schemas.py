from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class WatchesBase(BaseModel):
    name: str
    producer_id: int
    is_whatertightness: bool = False
    released_at: datetime
    size_milimetrs: int = Field(ge=10, le=100)
    type: str = Field(pattern="^(electronical|mechanical|hybrid)$")
    count: int = Field(ge=0)
    gender: str = Field(pattern="^(unisex|male|female)$")
    price: float = Field(gt=0)


class WatchesCreate(WatchesBase):
    pass


class WatchesUpdate(BaseModel):
    name: Optional[str] = None
    producer_id: Optional[int] = None
    is_whatertightness: Optional[bool] = None
    released_at: Optional[datetime] = None
    size_milimetrs: Optional[int] = None
    type: Optional[str] = None
    count: Optional[int] = None
    gender: Optional[str] = None
    price: Optional[float] = None


class WatchesInfo(BaseModel):
    id: int
    name: str
    producer_id: int
    is_whatertightness: bool
    released_at: datetime
    size_milimetrs: int
    type: str
    count: int
    gender: str
    price: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
