from typing import Optional

from pydantic import BaseModel, EmailStr

class UsersBase(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    email: str
    password: str
    is_active: bool = False
    is_admin: bool = False

class UsersCreate(UsersBase):
    pass

class UsersUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UsersInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    father_name: Optional[str]
    email: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True

class UsersLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsersInfo