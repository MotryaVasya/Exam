from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DiscountsBase(BaseModel):
    discount_code: str = Field(min_length=1, max_length=20)
    discount_percent: int = Field(ge=0, le=100)


class DiscountsCreate(DiscountsBase):
    pass


class DiscountsUpdate(BaseModel):
    discount_code: Optional[str] = None
    discount_percent: Optional[int] = None


class DiscountsInfo(BaseModel):
    id: int
    discount_code: str
    discount_percent: int

    class Config:
        from_attributes = True
