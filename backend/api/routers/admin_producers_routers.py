from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.producers_services import ProducersService
from services.admin_logs_services import log_admin_action
from db.schemas.producers_schemas import ProducersCreate, ProducersInfo, ProducersUpdate
from core.jwt import get_current_admin_user
from db.models import Users
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/producers', tags=['admin_producers'])


@router.get("/", response_model=list[ProducersInfo])
async def get_all_producers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str | None = Query(None, description="Поиск по названию"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список всех производителей с пагинацией. Требуется админ."""
    from sqlalchemy import select
    from db.models import Producers
    
    query = select(Producers).offset(skip).limit(limit)
    
    if search:
        query = query.where(Producers.name.ilike(f"%{search}%"))
    
    res = await db.execute(query)
    producers = res.scalars().all()
    
    return [
        ProducersInfo(
            id=p.id,
            name=p.name,
            created_at=p.created_at,
            updated_at=p.updated_at
        ) for p in producers
    ]


@router.get("/{producer_id}", response_model=ProducersInfo)
async def get_producer(
    producer_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить производителя по ID. Требуется админ."""
    service = ProducersService(database=db)
    producer = await service.get_producer(producer_id=producer_id)
    return producer


@router.post("/", response_model=ProducersInfo)
async def create_producer(
    producer_data: ProducersCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Создать нового производителя. Требуется админ."""
    service = ProducersService(database=db)
    producer = await service.create_producer(data=producer_data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="CREATE",
        entity="producers",
        entity_id=producer.id,
        description=f"Создан производитель {producer.name}",
        ip_address=request.client.host if request.client else None
    )
    
    return producer


@router.put("/{producer_id}", response_model=ProducersInfo)
async def update_producer(
    producer_id: int,
    data: ProducersUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить производителя. Требуется админ."""
    service = ProducersService(database=db)
    producer = await service.update_producer(producer_id=producer_id, data=data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="producers",
        entity_id=producer_id,
        description=f"Обновлен производитель {producer.name}",
        ip_address=request.client.host if request.client else None
    )
    
    return producer


@router.delete("/{producer_id}")
async def delete_producer(
    producer_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить производителя. Требуется админ."""
    service = ProducersService(database=db)
    result = await service.delete_producer(producer_id=producer_id)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="producers",
        entity_id=producer_id,
        description=f"Удалён производитель с ID {producer_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return result


@router.delete("/batch")
async def batch_delete_producers(
    request: Request,
    producer_ids: list[int] = Query(..., description="Список ID производителей для удаления"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Массовое удаление производителей. Требуется админ."""
    service = ProducersService(database=db)
    deleted_count = 0
    
    for pid in producer_ids:
        try:
            await service.delete_producer(producer_id=pid)
            deleted_count += 1
        except Exception as e:
            log.error(f"Не удалось удалить производителя {pid}: {e}")
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="producers",
        description=f"Массовое удаление: удалено {deleted_count} из {len(producer_ids)} производителей",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Удалено {deleted_count} из {len(producer_ids)} производителей", "deleted_count": deleted_count}
