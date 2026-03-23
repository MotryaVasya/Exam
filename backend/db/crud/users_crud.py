from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Users
from db.schemas.users_schemas import UsersCreate, UsersInfo
from core.config import context
from logging import Logger

log = Logger(__name__)

async def hash_pass(password: str) -> str:
    return context.hash(password)

async def veify_password(plain_pass: str, hash_pass) -> bool:
    return context.verify(plain_pass, hash_pass)

async def create(db: AsyncSession, data: UsersCreate) -> Users:
    try:
        if await db.execute(select(Users).where(Users.email == data.email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с такой почтой уже существует"
            )
        
        if len(data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль слишком маленький, минимум 8 символов"
            )
        
        # Добавить еще несколько проверок на пользователя

        user = Users(
            first_name=data.first_name,
            last_name=data.last_name,
            father_name=data.father_name,
            email=data.email,
            password=await hash_pass(data.password),
            is_active=data.is_active
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        await log.info(msg={
            "message": "Пользователь успешно создан!"
        })
        return user 
    
    except Exception as e:
        await db.rollback()
        await log.error(msg={
            "message": str(e),
            "data_user": data.model_dump()
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )

async def get(db: AsyncSession, user_id: int) -> Users | object:
    if user_id <= 0:
        return {
            "message": "ID меньше одного, такого не может быть!"
        }
    try:
        res = await db.execute(select(Users).where(Users.id == user_id))
        user = await res.scalar_one_or_none()
        if not user:
            return {
                "message": "Такого пользователя не существует!"
            }
        return user
    except Exception as e:
        await log.error(msg={
            "message": str(e),
            "user_id": user_id
        })

async def update():
    pass

async def delete():
    pass

async def login():
    pass