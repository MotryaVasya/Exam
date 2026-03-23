from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.orders_schemas import OrdersCreate, OrdersInfo, OrdersUpdate
from db.crud.orders_crud import create, get, get_by_user_id, get_all, update, delete, get_total_count
import logging

log = logging.getLogger(__name__)


class OrdersService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_order(self, data: OrdersCreate) -> OrdersInfo:
        order = await create(db=self.db, data=data)
        return OrdersInfo(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            discount=order.discount,
            is_pickup=order.is_pickup,
            delivery_address=order.delivery_address,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    async def get_order(self, order_id: int) -> OrdersInfo:
        order = await get(db=self.db, order_id=order_id)
        return OrdersInfo(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            discount=order.discount,
            is_pickup=order.is_pickup,
            delivery_address=order.delivery_address,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    async def get_orders_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OrdersInfo]:
        orders = await get_by_user_id(db=self.db, user_id=user_id, skip=skip, limit=limit)
        return [
            OrdersInfo(
                id=o.id,
                user_id=o.user_id,
                total_price=o.total_price,
                discount=o.discount,
                is_pickup=o.is_pickup,
                delivery_address=o.delivery_address,
                created_at=o.created_at,
                updated_at=o.updated_at
            ) for o in orders
        ]

    async def get_all_orders(self, skip: int = 0, limit: int = 100) -> list[OrdersInfo]:
        orders = await get_all(db=self.db, skip=skip, limit=limit)
        return [
            OrdersInfo(
                id=o.id,
                user_id=o.user_id,
                total_price=o.total_price,
                discount=o.discount,
                is_pickup=o.is_pickup,
                delivery_address=o.delivery_address,
                created_at=o.created_at,
                updated_at=o.updated_at
            ) for o in orders
        ]

    async def update_order(self, order_id: int, data: OrdersUpdate) -> OrdersInfo:
        order = await update(db=self.db, order_id=order_id, data=data)
        return OrdersInfo(
            id=order.id,
            user_id=order.user_id,
            total_price=order.total_price,
            discount=order.discount,
            is_pickup=order.is_pickup,
            delivery_address=order.delivery_address,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    async def delete_order(self, order_id: int) -> dict:
        result = await delete(db=self.db, order_id=order_id)
        return {"message": "Заказ успешно удалён", "success": result}

    async def get_orders_count(self, user_id: int | None = None) -> int:
        return await get_total_count(db=self.db, user_id=user_id)
