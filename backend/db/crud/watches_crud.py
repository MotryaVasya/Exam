from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Watches
from db.schemas.watches_schemas import WatchesCreate, WatchesUpdate
from datetime import datetime
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: WatchesCreate) -> Watches:
    try:
        watch = Watches(
            name=data.name,
            producer_id=data.producer_id,
            is_whatertightness=data.is_whatertightness,
            released_at=data.released_at,
            size_milimetrs=data.size_milimetrs,
            type=data.type,
            count=data.count,
            gender=data.gender,
            price=data.price,
            image_url=data.image_url,
            updated_at=datetime.now()
        )
        db.add(watch)
        await db.commit()
        await db.refresh(watch)
        log.info("Часы успешно созданы!")
        return watch

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании часов: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании часов: {str(e)}"
        )


async def get(db: AsyncSession, watch_id: int) -> Watches:
    if watch_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID часов невозможен!"
        )
    try:
        res = await db.execute(select(Watches).where(Watches.id == watch_id))
        watch = res.scalar_one_or_none()
        if not watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Таких часов не существует!"
            )
        log.info("Часы успешно найдены!")
        return watch
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении часов: {e}, watch_id: {watch_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении часов: {str(e)}"
        )


async def get_all(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    producer_id: int | None = None,
    type: str | None = None,
    gender: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
) -> list[Watches]:
    try:
        query = select(Watches)
        
        if producer_id:
            query = query.where(Watches.producer_id == producer_id)
        if type:
            query = query.where(Watches.type == type)
        if gender:
            query = query.where(Watches.gender == gender)
        if min_price is not None:
            query = query.where(Watches.price >= min_price)
        if max_price is not None:
            query = query.where(Watches.price <= max_price)
        
        query = query.offset(skip).limit(limit)
        res = await db.execute(query)
        watches = res.scalars().all()
        log.info(f"Получено {len(watches)} часов")
        return watches
    except Exception as e:
        log.error(f"Ошибка при получении списка часов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка часов: {str(e)}"
        )


async def update(db: AsyncSession, watch_id: int, data: WatchesUpdate) -> Watches:
    if watch_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID часов невозможен!"
        )
    try:
        res = await db.execute(select(Watches).where(Watches.id == watch_id))
        watch = res.scalar_one_or_none()
        if not watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Таких часов не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(watch, key, value)

        await db.commit()
        await db.refresh(watch)
        log.info("Часы успешно обновлены!")
        return watch
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении часов с ID {watch_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении часов: {str(e)}"
        )


async def delete(db: AsyncSession, watch_id: int) -> bool:
    if watch_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID часов невозможен!"
        )
    try:
        res = await db.execute(select(Watches).where(Watches.id == watch_id))
        watch = res.scalar_one_or_none()

        if not watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Таких часов не существует!"
            )
        await db.delete(watch)
        await db.commit()
        log.info("Часы успешно удалены!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении часов с ID {watch_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении часов: {str(e)}"
        )
