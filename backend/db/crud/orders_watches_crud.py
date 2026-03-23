from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import OrdersWatches
from db.schemas.orders_watches_schemas import OrdersWatchesCreate, OrdersWatchesUpdate
from datetime import datetime
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: OrdersWatchesCreate) -> OrdersWatches:
    try:
        order_watch = OrdersWatches(
            order_id=data.order_id,
            watch_id=data.watch_id,
            updated_at=datetime.now()
        )
        db.add(order_watch)
        await db.commit()
        await db.refresh(order_watch)
        log.info("Связь заказа и часов успешно создана!")
        return order_watch

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании связи заказа и часов: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании связи заказа и часов: {str(e)}"
        )


async def get(db: AsyncSession, id: int) -> OrdersWatches:
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID связи невозможен!"
        )
    try:
        res = await db.execute(select(OrdersWatches).where(OrdersWatches.id == id))
        order_watch = res.scalar_one_or_none()
        if not order_watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой связи заказа и часов не существует!"
            )
        log.info("Связь заказа и часов успешно найдена!")
        return order_watch
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении связи заказа и часов: {e}, id: {id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении связи заказа и часов: {str(e)}"
        )


async def get_by_order_id(db: AsyncSession, order_id: int) -> list[OrdersWatches]:
    """Получает все часы в заказе."""
    try:
        res = await db.execute(
            select(OrdersWatches).where(OrdersWatches.order_id == order_id)
        )
        order_watches = res.scalars().all()
        log.info(f"Получено {len(order_watches)} часов в заказе {order_id}")
        return order_watches
    except Exception as e:
        log.error(f"Ошибка при получении часов заказа: {e}, order_id: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении часов заказа: {str(e)}"
        )


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[OrdersWatches]:
    try:
        res = await db.execute(select(OrdersWatches).offset(skip).limit(limit))
        order_watches = res.scalars().all()
        log.info(f"Получено {len(order_watches)} связей заказов и часов")
        return order_watches
    except Exception as e:
        log.error(f"Ошибка при получении списка связей заказов и часов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка связей заказов и часов: {str(e)}"
        )


async def update(db: AsyncSession, id: int, data: OrdersWatchesUpdate) -> OrdersWatches:
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID связи невозможен!"
        )
    try:
        res = await db.execute(select(OrdersWatches).where(OrdersWatches.id == id))
        order_watch = res.scalar_one_or_none()
        if not order_watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой связи заказа и часов не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order_watch, key, value)

        await db.commit()
        await db.refresh(order_watch)
        log.info("Связь заказа и часов успешно обновлена!")
        return order_watch
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении связи заказа и часов с ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении связи заказа и часов: {str(e)}"
        )


async def delete(db: AsyncSession, id: int) -> bool:
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID связи невозможен!"
        )
    try:
        res = await db.execute(select(OrdersWatches).where(OrdersWatches.id == id))
        order_watch = res.scalar_one_or_none()

        if not order_watch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой связи заказа и часов не существует!"
            )
        await db.delete(order_watch)
        await db.commit()
        log.info("Связь заказа и часов успешно удалена!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении связи заказа и часов с ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении связи заказа и часов: {str(e)}"
        )


async def delete_by_order_id(db: AsyncSession, order_id: int) -> bool:
    """Удаляет все связи заказа с часами."""
    try:
        order_watches = await get_by_order_id(db, order_id)
        for order_watch in order_watches:
            await db.delete(order_watch)
        await db.commit()
        log.info(f"Все связи заказа {order_id} с часами успешно удалены!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении связей заказа {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении связей заказа: {str(e)}"
        )
