from typing import Optional

from pydantic import BaseModel

class UsersBase(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str]
    email: str
    password: str
    is_active: bool = False

class UsersCreate(UsersBase):
    pass 

class UsersUpdate(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str]
    email: str
    password: str

class UsersInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    father_name: Optional[str]
    email: str
    is_active: str