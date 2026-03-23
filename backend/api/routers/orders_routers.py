from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.orders_services import OrdersService
from db.schemas.orders_schemas import OrdersCreate, OrdersInfo, OrdersUpdate
from core.jwt import get_current_user
from db.schemas.users_schemas import UsersInfo

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post("/", response_model=OrdersInfo)
async def create_order(
    order_data: OrdersCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Создать новый заказ. Требуется авторизация."""
    service = OrdersService(database=db)
    order = await service.create_order(data=order_data)
    return order


@router.get("/", response_model=list[OrdersInfo])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить список всех заказов. Требуется авторизация."""
    service = OrdersService(database=db)
    orders = await service.get_all_orders(skip=skip, limit=limit)
    return orders


@router.get("/my", response_model=list[OrdersInfo])
async def get_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить мои заказы. Требуется авторизация."""
    service = OrdersService(database=db)
    orders = await service.get_orders_by_user_id(user_id=current_user.id, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrdersInfo)
async def get_order(
    order_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить заказ по ID. Требуется авторизация."""
    service = OrdersService(database=db)
    order = await service.get_order(order_id=order_id)
    return order


@router.put("/{order_id}", response_model=OrdersInfo)
async def update_order(
    order_id: int, 
    data: OrdersUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Обновить заказ. Требуется авторизация."""
    service = OrdersService(database=db)
    order = await service.update_order(order_id=order_id, data=data)
    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Удалить заказ. Требуется авторизация."""
    service = OrdersService(database=db)
    result = await service.delete_order(order_id=order_id)
    return result


@router.get("/count/my")
async def get_my_orders_count(
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить количество моих заказов. Требуется авторизация."""
    service = OrdersService(database=db)
    count = await service.get_orders_count(user_id=current_user.id)
    return {"user_id": current_user.id, "orders_count": count}
