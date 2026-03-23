from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import VerificationCodes
from db.schemas.verification_codes_schemas import VerificationCodesCreate, VerificationCodesUpdate
from datetime import datetime
import logging
import random

log = logging.getLogger(__name__)


def generate_code() -> int:
    """Генерирует 4-значный код верификации."""
    return random.randint(1000, 9999)


async def create(db: AsyncSession, data: VerificationCodesCreate) -> VerificationCodes:
    try:
        # Удаляем старые коды пользователя
        await db.execute(
            select(VerificationCodes)
            .where(VerificationCodes.user_id == data.user_id)
        )
        
        code = VerificationCodes(
            user_id=data.user_id,
            code=data.code if data.code else generate_code(),
            updated_at=datetime.now()
        )
        db.add(code)
        await db.commit()
        await db.refresh(code)
        log.info("Код верификации успешно создан!")
        return code

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании кода верификации: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании кода верификации: {str(e)}"
        )


async def get(db: AsyncSession, code_id: int) -> VerificationCodes:
    if code_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID кода невозможен!"
        )
    try:
        res = await db.execute(select(VerificationCodes).where(VerificationCodes.id == code_id))
        code = res.scalar_one_or_none()
        if not code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого кода верификации не существует!"
            )
        log.info("Код верификации успешно найден!")
        return code
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении кода верификации: {e}, code_id: {code_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении кода верификации: {str(e)}"
        )


async def get_by_user_id(db: AsyncSession, user_id: int) -> VerificationCodes | None:
    try:
        res = await db.execute(
            select(VerificationCodes)
            .where(VerificationCodes.user_id == user_id)
            .order_by(VerificationCodes.created_at.desc())
        )
        code = res.scalar_one_or_none()
        return code
    except Exception as e:
        log.error(f"Ошибка при получении кода верификации пользователя: {e}, user_id: {user_id}")
        return None


async def verify_code(db: AsyncSession, user_id: int, code: int) -> bool:
    """Проверяет код верификации."""
    try:
        verification_code = await get_by_user_id(db, user_id)
        if not verification_code:
            return False
        
        if verification_code.code != code:
            return False
        
        # Удаляем использованный код
        await db.delete(verification_code)
        await db.commit()
        log.info(f"Код верификации для пользователя {user_id} успешно подтверждён!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при проверке кода верификации: {e}, user_id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при проверке кода верификации: {str(e)}"
        )


async def update(db: AsyncSession, code_id: int, data: VerificationCodesUpdate) -> VerificationCodes:
    if code_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID кода невозможен!"
        )
    try:
        res = await db.execute(select(VerificationCodes).where(VerificationCodes.id == code_id))
        code = res.scalar_one_or_none()
        if not code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого кода верификации не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(code, key, value)

        await db.commit()
        await db.refresh(code)
        log.info("Код верификации успешно обновлен!")
        return code
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении кода верификации с ID {code_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении кода верификации: {str(e)}"
        )


async def delete(db: AsyncSession, code_id: int) -> bool:
    if code_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID кода невозможен!"
        )
    try:
        res = await db.execute(select(VerificationCodes).where(VerificationCodes.id == code_id))
        code = res.scalar_one_or_none()

        if not code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого кода верификации не существует!"
            )
        await db.delete(code)
        await db.commit()
        log.info("Код верификации успешно удален!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении кода верификации с ID {code_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении кода верификации: {str(e)}"
        )


async def delete_by_user_id(db: AsyncSession, user_id: int) -> bool:
    """Удаляет все коды верификации пользователя."""
    try:
        codes = await db.execute(
            select(VerificationCodes).where(VerificationCodes.user_id == user_id)
        )
        codes_list = codes.scalars().all()
        
        for code in codes_list:
            await db.delete(code)
        
        await db.commit()
        log.info(f"Все коды верификации пользователя {user_id} успешно удалены!")
        return True
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении кодов верификации пользователя {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении кодов верификации: {str(e)}"
        )
