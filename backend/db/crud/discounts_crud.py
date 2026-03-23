from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Discounts
from db.schemas.discounts_schemas import DiscountsCreate, DiscountsUpdate
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: DiscountsCreate) -> Discounts:
    try:
        check = await db.execute(select(Discounts).where(Discounts.discount_code == data.discount_code))
        if check.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Скидка с таким кодом уже существует"
            )

        discount = Discounts(
            discount_code=data.discount_code,
            discount_percent=data.discount_percent
        )
        db.add(discount)
        await db.commit()
        await db.refresh(discount)
        log.info("Скидка успешно создана!")
        return discount

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании скидки: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании скидки: {str(e)}"
        )


async def get(db: AsyncSession, discount_id: int) -> Discounts:
    if discount_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID скидки невозможен!"
        )
    try:
        res = await db.execute(select(Discounts).where(Discounts.id == discount_id))
        discount = res.scalar_one_or_none()
        if not discount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой скидки не существует!"
            )
        log.info("Скидка успешно найдена!")
        return discount
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении скидки: {e}, discount_id: {discount_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении скидки: {str(e)}"
        )


async def get_by_code(db: AsyncSession, discount_code: str) -> Discounts | None:
    try:
        res = await db.execute(select(Discounts).where(Discounts.discount_code == discount_code))
        discount = res.scalar_one_or_none()
        return discount
    except Exception as e:
        log.error(f"Ошибка при получении скидки по коду: {e}, discount_code: {discount_code}")
        return None


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Discounts]:
    try:
        res = await db.execute(select(Discounts).offset(skip).limit(limit))
        discounts = res.scalars().all()
        log.info(f"Получено {len(discounts)} скидок")
        return discounts
    except Exception as e:
        log.error(f"Ошибка при получении списка скидок: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка скидок: {str(e)}"
        )


async def update(db: AsyncSession, discount_id: int, data: DiscountsUpdate) -> Discounts:
    if discount_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID скидки невозможен!"
        )
    try:
        res = await db.execute(select(Discounts).where(Discounts.id == discount_id))
        discount = res.scalar_one_or_none()
        if not discount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой скидки не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(discount, key, value)

        await db.commit()
        await db.refresh(discount)
        log.info("Скидка успешно обновлена!")
        return discount
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении скидки с ID {discount_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении скидки: {str(e)}"
        )


async def delete(db: AsyncSession, discount_id: int) -> bool:
    if discount_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID скидки невозможен!"
        )
    try:
        res = await db.execute(select(Discounts).where(Discounts.id == discount_id))
        discount = res.scalar_one_or_none()

        if not discount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой скидки не существует!"
            )
        await db.delete(discount)
        await db.commit()
        log.info("Скидка успешно удалена!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении скидки с ID {discount_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении скидки: {str(e)}"
        )
