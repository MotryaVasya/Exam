from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.orders_services import OrdersService
from services.admin_logs_services import log_admin_action
from db.schemas.orders_schemas import OrdersCreate, OrdersInfo, OrdersUpdate
from core.jwt import get_current_admin_user
from db.models import Orders, Users
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/orders', tags=['admin_orders'])


@router.get("/", response_model=list[OrdersInfo])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: int | None = Query(None),
    is_pickup: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список всех заказов с фильтрацией и пагинацией. Требуется админ."""
    from sqlalchemy import select
    from db.models import Orders
    
    query = select(Orders).offset(skip).limit(limit)
    
    if user_id:
        query = query.where(Orders.user_id == user_id)
    if is_pickup is not None:
        query = query.where(Orders.is_pickup == is_pickup)
    
    res = await db.execute(query)
    orders = res.scalars().all()
    
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


@router.get("/count")
async def get_orders_count(
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить общее количество заказов. Требуется админ."""
    from sqlalchemy import func, select
    query = select(func.count(Orders.id))
    res = await db.execute(query)
    count = res.scalar()
    return {"total_orders": count or 0}


@router.get("/{order_id}", response_model=OrdersInfo)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить заказ по ID. Требуется админ."""
    service = OrdersService(database=db)
    order = await service.get_order(order_id=order_id)
    return order


@router.post("/", response_model=OrdersInfo)
async def create_order(
    order_data: OrdersCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Создать новый заказ. Требуется админ."""
    service = OrdersService(database=db)
    order = await service.create_order(data=order_data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="CREATE",
        entity="orders",
        entity_id=order.id,
        description=f"Создан заказ на сумму {order.total_price}",
        ip_address=request.client.host if request.client else None
    )
    
    return order


@router.put("/{order_id}", response_model=OrdersInfo)
async def update_order(
    order_id: int,
    data: OrdersUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить заказ. Требуется админ."""
    service = OrdersService(database=db)
    order = await service.update_order(order_id=order_id, data=data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="orders",
        entity_id=order_id,
        description=f"Обновлен заказ {order_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить заказ. Требуется админ."""
    service = OrdersService(database=db)
    result = await service.delete_order(order_id=order_id)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="orders",
        entity_id=order_id,
        description=f"Удалён заказ с ID {order_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return result


@router.delete("/batch")
async def batch_delete_orders(
    request: Request,
    order_ids: list[int] = Query(..., description="Список ID заказов для удаления"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Массовое удаление заказов. Требуется админ."""
    service = OrdersService(database=db)
    deleted_count = 0
    
    for oid in order_ids:
        try:
            await service.delete_order(order_id=oid)
            deleted_count += 1
        except Exception as e:
            log.error(f"Не удалось удалить заказ {oid}: {e}")
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="orders",
        description=f"Массовое удаление: удалено {deleted_count} из {len(order_ids)} заказов",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Удалено {deleted_count} из {len(order_ids)} заказов", "deleted_count": deleted_count}
