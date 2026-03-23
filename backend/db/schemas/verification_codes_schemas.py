from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VerificationCodesBase(BaseModel):
    user_id: int
    code: int


class VerificationCodesCreate(VerificationCodesBase):
    pass


class VerificationCodesUpdate(BaseModel):
    user_id: Optional[int] = None
    code: Optional[int] = None


class VerificationCodesInfo(BaseModel):
    id: int
    user_id: int
    code: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
