from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AdminLogsBase(BaseModel):
    admin_id: Optional[int] = None
    action: str
    entity: str
    entity_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None


class AdminLogsCreate(AdminLogsBase):
    pass


class AdminLogsUpdate(BaseModel):
    admin_id: Optional[int] = None
    action: Optional[str] = None
    entity: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None


class AdminLogsInfo(BaseModel):
    id: int
    admin_id: Optional[int] = None
    action: str
    entity: str
    entity_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
