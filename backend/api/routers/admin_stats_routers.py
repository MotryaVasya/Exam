from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from core.jwt import get_current_admin_user
from db.models import Users, Orders, Watches, Producers, Discounts
from sqlalchemy import func, select
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/stats', tags=['admin_stats'])


@router.get("/")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить общую статистику. Требуется админ."""
    
    # Количество пользователей
    users_count = await db.execute(select(func.count(Users.id)))
    users_total = users_count.scalar() or 0
    
    users_active = await db.execute(select(func.count(Users.id)).where(Users.is_active == True))
    users_active_count = users_active.scalar() or 0
    
    users_admin = await db.execute(select(func.count(Users.id)).where(Users.is_admin == True))
    users_admin_count = users_admin.scalar() or 0
    
    # Количество заказов и сумма
    orders_count = await db.execute(select(func.count(Orders.id)))
    orders_total = orders_count.scalar() or 0
    
    orders_sum = await db.execute(select(func.sum(Orders.total_price)))
    orders_total_sum = orders_sum.scalar() or 0
    
    orders_avg = await db.execute(select(func.avg(Orders.total_price)))
    orders_avg_price = orders_avg.scalar() or 0
    
    # Количество товаров
    watches_count = await db.execute(select(func.count(Watches.id)))
    watches_total = watches_count.scalar() or 0
    
    watches_stock = await db.execute(select(func.sum(Watches.count)))
    watches_in_stock = watches_stock.scalar() or 0
    
    # Количество производителей
    producers_count = await db.execute(select(func.count(Producers.id)))
    producers_total = producers_count.scalar() or 0
    
    # Количество скидок
    discounts_count = await db.execute(select(func.count(Discounts.id)))
    discounts_total = discounts_count.scalar() or 0
    
    return {
        "users": {
            "total": users_total,
            "active": users_active_count,
            "admins": users_admin_count
        },
        "orders": {
            "total": orders_total,
            "total_revenue": float(orders_total_sum),
            "average_order_price": float(orders_avg_price) if orders_avg_price else 0
        },
        "watches": {
            "total_products": watches_total,
            "total_in_stock": watches_in_stock
        },
        "producers": {
            "total": producers_total
        },
        "discounts": {
            "total": discounts_total
        }
    }


@router.get("/revenue")
async def get_revenue_stats(
    period: str = Query("all", description="all, today, week, month"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить статистику выручки. Требуется админ."""
    from datetime import datetime, timedelta
    
    now = datetime.now()
    
    if period == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now - timedelta(days=30)
    else:
        start_date = None
    
    query = select(func.sum(Orders.total_price))
    if start_date:
        query = query.where(Orders.created_at >= start_date)
    
    result = await db.execute(query)
    revenue = result.scalar() or 0
    
    # Количество заказов за период
    orders_query = select(func.count(Orders.id))
    if start_date:
        orders_query = orders_query.where(Orders.created_at >= start_date)
    
    orders_result = await db.execute(orders_query)
    orders_count = orders_result.scalar() or 0
    
    return {
        "period": period,
        "revenue": float(revenue),
        "orders_count": orders_count
    }


@router.get("/top-products")
async def get_top_products(
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить топ популярных товаров. Требуется админ."""
    from db.models import OrdersWatches
    from sqlalchemy import desc
    
    query = (
        select(
            Watches.id,
            Watches.name,
            func.count(OrdersWatches.watch_id).label("order_count")
        )
        .join(OrdersWatches, Watches.id == OrdersWatches.watch_id)
        .group_by(Watches.id, Watches.name)
        .order_by(desc("order_count"))
        .limit(limit)
    )
    
    result = await db.execute(query)
    top_products = result.fetchall()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "orders_count": p.order_count
        } for p in top_products
    ]
