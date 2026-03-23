from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Users
from db.schemas.users_schemas import UsersCreate, UsersInfo, UsersUpdate, UsersLogin, Token
from db.session import get_db
from services.users_services import UsersService
from core.jwt import get_current_user as get_current_user_from_db


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/", response_model=UsersInfo)
async def post(user_data: UsersCreate, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    user = await service.create_user(data=user_data)
    return user

@router.post("/login", response_model=Token)
async def login(user_data: UsersLogin, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    token = await service.login_user(email=user_data.email, password=user_data.password)
    return token

@router.get('/me', response_model=UsersInfo)
async def get_current_user_info(current_user: Users = Depends(get_current_user_from_db)):
    """Получить информацию о текущем авторизованном пользователе."""
    return UsersInfo(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        father_name=current_user.father_name or None,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin
    )

@router.get('/{user_id}', response_model=UsersInfo)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    user = await service.get_user(user_id=user_id)
    return user

@router.put('/{user_id}', response_model=UsersInfo)
async def put(user_id: int, data: UsersUpdate, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    user = await service.update_user(user_id=user_id, data=data)
    return user

@router.patch("/{user_id}", response_model=UsersInfo)
async def update_status(user_id: int, is_active: bool = True, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    user = await service.udpate_status_user(user_id=user_id, status=is_active)
    return user

@router.delete("/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UsersService(database=db)
    result = await service.delete_user(user_id=user_id)
    return result
