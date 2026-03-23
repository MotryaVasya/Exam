from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import Orders
from db.schemas.orders_schemas import OrdersCreate, OrdersUpdate
from datetime import datetime
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: OrdersCreate) -> Orders:
    try:
        order = Orders(
            user_id=data.user_id,
            total_price=data.total_price,
            discount=data.discount,
            is_pickup=data.is_pickup,
            delivery_address=data.delivery_address,
            updated_at=datetime.now()
        )
        db.add(order)
        await db.commit()
        await db.refresh(order)
        log.info("Заказ успешно создан!")
        return order

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании заказа: {e}, данные: {data.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании заказа: {str(e)}"
        )


async def get(db: AsyncSession, order_id: int) -> Orders:
    if order_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID заказа невозможен!"
        )
    try:
        res = await db.execute(select(Orders).where(Orders.id == order_id))
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого заказа не существует!"
            )
        log.info("Заказ успешно найден!")
        return order
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении заказа: {e}, order_id: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении заказа: {str(e)}"
        )


async def get_by_user_id(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[Orders]:
    try:
        res = await db.execute(
            select(Orders)
            .where(Orders.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        orders = res.scalars().all()
        log.info(f"Получено {len(orders)} заказов пользователя {user_id}")
        return orders
    except Exception as e:
        log.error(f"Ошибка при получении заказов пользователя: {e}, user_id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении заказов: {str(e)}"
        )


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Orders]:
    try:
        res = await db.execute(select(Orders).offset(skip).limit(limit))
        orders = res.scalars().all()
        log.info(f"Получено {len(orders)} заказов")
        return orders
    except Exception as e:
        log.error(f"Ошибка при получении списка заказов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка заказов: {str(e)}"
        )


async def update(db: AsyncSession, order_id: int, data: OrdersUpdate) -> Orders:
    if order_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID заказа невозможен!"
        )
    try:
        res = await db.execute(select(Orders).where(Orders.id == order_id))
        order = res.scalar_one_or_none()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого заказа не существует!"
            )

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order, key, value)

        await db.commit()
        await db.refresh(order)
        log.info("Заказ успешно обновлен!")
        return order
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при обновлении заказа с ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении заказа: {str(e)}"
        )


async def delete(db: AsyncSession, order_id: int) -> bool:
    if order_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID заказа невозможен!"
        )
    try:
        res = await db.execute(select(Orders).where(Orders.id == order_id))
        order = res.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого заказа не существует!"
            )
        await db.delete(order)
        await db.commit()
        log.info("Заказ успешно удален!")
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении заказа с ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении заказа: {str(e)}"
        )


async def get_total_count(db: AsyncSession, user_id: int | None = None) -> int:
    """Получает общее количество заказов."""
    try:
        query = select(func.count(Orders.id))
        if user_id:
            query = query.where(Orders.user_id == user_id)
        result = await db.execute(query)
        count = result.scalar()
        return count or 0
    except Exception as e:
        log.error(f"Ошибка при подсчёте заказов: {e}")
        return 0
