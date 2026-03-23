from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.orders_watches_schemas import OrdersWatchesCreate, OrdersWatchesInfo, OrdersWatchesUpdate
from db.crud.orders_watches_crud import (
    create, get, get_by_order_id, get_all, update, delete, delete_by_order_id
)
import logging

log = logging.getLogger(__name__)


class OrdersWatchesService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_order_watch(self, data: OrdersWatchesCreate) -> OrdersWatchesInfo:
        order_watch = await create(db=self.db, data=data)
        return OrdersWatchesInfo(
            id=order_watch.id,
            order_id=order_watch.order_id,
            watch_id=order_watch.watch_id,
            created_at=order_watch.created_at,
            updated_at=order_watch.updated_at
        )

    async def get_order_watch(self, id: int) -> OrdersWatchesInfo:
        order_watch = await get(db=self.db, id=id)
        return OrdersWatchesInfo(
            id=order_watch.id,
            order_id=order_watch.order_id,
            watch_id=order_watch.watch_id,
            created_at=order_watch.created_at,
            updated_at=order_watch.updated_at
        )

    async def get_order_watches_by_order_id(self, order_id: int) -> list[OrdersWatchesInfo]:
        order_watches = await get_by_order_id(db=self.db, order_id=order_id)
        return [
            OrdersWatchesInfo(
                id=ow.id,
                order_id=ow.order_id,
                watch_id=ow.watch_id,
                created_at=ow.created_at,
                updated_at=ow.updated_at
            ) for ow in order_watches
        ]

    async def get_all_order_watches(self, skip: int = 0, limit: int = 100) -> list[OrdersWatchesInfo]:
        order_watches = await get_all(db=self.db, skip=skip, limit=limit)
        return [
            OrdersWatchesInfo(
                id=ow.id,
                order_id=ow.order_id,
                watch_id=ow.watch_id,
                created_at=ow.created_at,
                updated_at=ow.updated_at
            ) for ow in order_watches
        ]

    async def update_order_watch(self, id: int, data: OrdersWatchesUpdate) -> OrdersWatchesInfo:
        order_watch = await update(db=self.db, id=id, data=data)
        return OrdersWatchesInfo(
            id=order_watch.id,
            order_id=order_watch.order_id,
            watch_id=order_watch.watch_id,
            created_at=order_watch.created_at,
            updated_at=order_watch.updated_at
        )

    async def delete_order_watch(self, id: int) -> dict:
        result = await delete(db=self.db, id=id)
        return {"message": "Связь заказа и часов успешно удалена", "success": result}

    async def delete_order_watches_by_order_id(self, order_id: int) -> dict:
        result = await delete_by_order_id(db=self.db, order_id=order_id)
        return {"message": "Все связи заказа с часами успешно удалены", "success": result}
