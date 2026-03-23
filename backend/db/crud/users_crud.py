from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Users
from db.schemas.users_schemas import UsersCreate, UsersInfo, UsersUpdate, UsersLogin
from core.config import context
from core.jwt import create_access_token
import logging

log = logging.getLogger(__name__)


async def hash_pass(password: str) -> str:
    return context.hash(password)

async def veify_password(plain_pass: str, hash_pass) -> bool:
    return context.verify(plain_pass, hash_pass)

async def create(db: AsyncSession, data: UsersCreate) -> Users:
    try:
        check = await db.execute(select(Users).where(Users.email == data.email))
        if check.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с такой почтой уже существует"
            )
        
        if len(data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль слишком маленький, минимум 8 символов"
            )
        
        # TODO Добавить еще несколько проверок на пользователя

        user = Users(
            first_name=data.first_name,
            last_name=data.last_name,
            father_name=data.father_name or None,
            email=data.email,
            password=await hash_pass(data.password),
            is_active=data.is_active,
            is_admin=data.is_admin
        )
        # TODO Отправить сообщение на почту SMTP
        db.add(user)
        await db.commit()
        await db.refresh(user)
        log.info("Пользователь успешно создан!")
        return user

    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании пользователя: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )

async def get(db: AsyncSession, user_id: int) -> Users:
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID пользователя невозможен!"
        )
    try:
        res = await db.execute(select(Users).where(Users.id == user_id))
        user = res.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого пользователя не существует!"
            )
        log.info("Пользователь успешно вернулся!")
        return user
    except Exception as e:
        log.error(msg={
            "message": "Ошибка при получения пользователя: " + str(e),
            "user_id": user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получения пользователя: {str(e)}"
        )

async def update(db: AsyncSession, user_id: int, data: UsersUpdate) -> Users:
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID пользователя невозможен!"
        )
    try:
        res = await db.execute(select(Users).where(Users.id == user_id))
        user = res.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого пользователя не существует!"
            )
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if key == "password":
                value = await hash_pass(value)
            setattr(user, key, value)
        
        await db.commit()
        await db.refresh(user)
        log.info(f"Пользователь успешно обновлен!")
        return user
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении пользователя с ID {user_id} на такие поля {data.model_dump()} {str(e)}")
        raise HTTPException(
            # TODO поменять потом на более улучшенную версию вывода правильного статус кода
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении пользоваетля {str(e)}"
            )

async def delete(db: AsyncSession, user_id: int) -> bool:
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID пользователя невозможен!"
        )   
    try:
        res = await db.execute(select(Users).where(Users.id == user_id))
        user = res.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого пользователя не существует!"
            )
        await db.delete(user)
        await db.commit()
        log.info("Пользователь успешно удален!")
        return True
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении пользователя с ID {user_id}")
        raise HTTPException(
            # TODO поменять потом на более улучшенную версию вывода правильного статус кода
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении пользоваетля {str(e)}"
            )
    
async def update_status(db: AsyncSession, user_id: int, status: bool = True) -> Users:
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID пользователя невозможен!"
        )   
    try:
        res = await db.execute(select(Users).where(Users.id == user_id))
        user = res.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого пользователя не существует!"
            )
        user.is_active = status
        await db.commit()
        await db.refresh(user)
        log.info("Пользователь успешно обновил свой статус!")
        return user
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении статуса пользователя с ID {user_id}")
        raise HTTPException(
            # TODO поменять потом на более улучшенную версию вывода правильного статус кода
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении статуса пользоваетля {str(e)}"
            )


async def login(db: AsyncSession, email: str, password: str) -> dict:
    """Проверяет логин/пароль и возвращает токен."""
    try:
        res = await db.execute(select(Users).where(Users.email == email))
        user = res.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт не активирован"
            )
        
        is_valid = await veify_password(password, user.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        
        access_token = create_access_token(data={"sub": user.id}, is_admin=user.is_admin)
        
        log.info(f"Пользователь {email} успешно вошёл в систему!")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при входе пользователя: {e}, email: {email}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при входе в систему: {str(e)}"
        )