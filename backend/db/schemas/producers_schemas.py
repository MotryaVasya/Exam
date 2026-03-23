from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProducersBase(BaseModel):
    name: str


class ProducersCreate(ProducersBase):
    pass


class ProducersUpdate(BaseModel):
    name: Optional[str] = None


class ProducersInfo(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
