from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Producers
from db.schemas.producers_schemas import ProducersCreate, ProducersUpdate
from datetime import datetime
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: ProducersCreate) -> Producers:
    try:
        check = await db.execute(select(Producers).where(Producers.name == data.name))
        if check.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Производитель с таким именем уже существует"
            )

        producer = Producers(
            name=data.name,
            updated_at=datetime.now()
        )
        db.add(producer)
        await db.commit()
        await db.refresh(producer)
        log.info("Производитель успешно создан!")
        return producer

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании производителя: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании производителя: {str(e)}"
        )


async def get(db: AsyncSession, producer_id: int) -> Producers:
    if producer_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID производителя невозможен!"
        )
    try:
        res = await db.execute(select(Producers).where(Producers.id == producer_id))
        producer = res.scalar_one_or_none()
        if not producer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого производителя не существует!"
            )
        log.info("Производитель успешно найден!")
        return producer
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении производителя: {e}, producer_id: {producer_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении производителя: {str(e)}"
        )


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Producers]:
    try:
        res = await db.execute(select(Producers).offset(skip).limit(limit))
        producers = res.scalars().all()
        log.info(f"Получено {len(producers)} производителей")
        return producers
    except Exception as e:
        log.error(f"Ошибка при получении списка производителей: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка производителей: {str(e)}"
        )


async def update(db: AsyncSession, producer_id: int, data: ProducersUpdate) -> Producers:
    if producer_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID производителя невозможен!"
        )
    try:
        res = await db.execute(select(Producers).where(Producers.id == producer_id))
        producer = res.scalar_one_or_none()
        if not producer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого производителя не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(producer, key, value)

        await db.commit()
        await db.refresh(producer)
        log.info(f"Производитель успешно обновлен!")
        return producer
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении производителя с ID {producer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении производителя: {str(e)}"
        )


async def delete(db: AsyncSession, producer_id: int) -> bool:
    if producer_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID производителя невозможен!"
        )
    try:
        res = await db.execute(select(Producers).where(Producers.id == producer_id))
        producer = res.scalar_one_or_none()

        if not producer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого производителя не существует!"
            )
        await db.delete(producer)
        await db.commit()
        log.info("Производитель успешно удален!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении производителя с ID {producer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении производителя: {str(e)}"
        )
