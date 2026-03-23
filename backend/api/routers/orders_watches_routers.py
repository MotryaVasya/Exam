from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.orders_watches_services import OrdersWatchesService
from db.schemas.orders_watches_schemas import OrdersWatchesCreate, OrdersWatchesInfo, OrdersWatchesUpdate
from core.jwt import get_current_user
from db.schemas.users_schemas import UsersInfo

router = APIRouter(prefix='/orders-watches', tags=['orders_watches'])


@router.post("/", response_model=OrdersWatchesInfo)
async def create_order_watch(
    order_watch_data: OrdersWatchesCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Добавить часы в заказ. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    order_watch = await service.create_order_watch(data=order_watch_data)
    return order_watch


@router.get("/", response_model=list[OrdersWatchesInfo])
async def get_all_order_watches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить список всех связей заказов и часов. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    order_watches = await service.get_all_order_watches(skip=skip, limit=limit)
    return order_watches


@router.get("/order/{order_id}", response_model=list[OrdersWatchesInfo])
async def get_order_watches_by_order_id(
    order_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить все часы в заказе. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    order_watches = await service.get_order_watches_by_order_id(order_id=order_id)
    return order_watches


@router.get("/{id}", response_model=OrdersWatchesInfo)
async def get_order_watch(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить связь заказа и часов по ID. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    order_watch = await service.get_order_watch(id=id)
    return order_watch


@router.put("/{id}", response_model=OrdersWatchesInfo)
async def update_order_watch(
    id: int, 
    data: OrdersWatchesUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Обновить связь заказа и часов. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    order_watch = await service.update_order_watch(id=id, data=data)
    return order_watch


@router.delete("/{id}")
async def delete_order_watch(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Удалить связь заказа и часов. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    result = await service.delete_order_watch(id=id)
    return result


@router.delete("/order/{order_id}")
async def delete_order_watches_by_order_id(
    order_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Удалить все связи заказа с часами. Требуется авторизация."""
    service = OrdersWatchesService(database=db)
    result = await service.delete_order_watches_by_order_id(order_id=order_id)
    return result
