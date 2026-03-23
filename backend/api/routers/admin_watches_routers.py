from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.watches_services import WatchesService
from services.admin_logs_services import log_admin_action
from db.schemas.watches_schemas import WatchesCreate, WatchesInfo, WatchesUpdate
from core.jwt import get_current_admin_user
from db.models import Users
from datetime import datetime
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/watches', tags=['admin_watches'])


@router.get("/", response_model=list[WatchesInfo])
async def get_all_watches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    producer_id: int | None = Query(None),
    type: str | None = Query(None),
    gender: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    search: str | None = Query(None, description="Поиск по названию"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список всех часов с фильтрацией и пагинацией. Требуется админ."""
    service = WatchesService(database=db)
    return await service.get_all_watches(
        skip=skip,
        limit=limit,
        producer_id=producer_id,
        type=type,
        gender=gender,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/{watch_id}", response_model=WatchesInfo)
async def get_watch(
    watch_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить часы по ID. Требуется админ."""
    service = WatchesService(database=db)
    watch = await service.get_watch(watch_id=watch_id)
    return watch


@router.post("/", response_model=WatchesInfo)
async def create_watch(
    watch_data: WatchesCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Создать новые часы. Требуется админ."""
    service = WatchesService(database=db)
    watch = await service.create_watch(data=watch_data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="CREATE",
        entity="watches",
        entity_id=watch.id,
        description=f"Созданы часы {watch.name} (производитель {watch.producer_id})",
        ip_address=request.client.host if request.client else None
    )
    
    return watch


@router.put("/{watch_id}", response_model=WatchesInfo)
async def update_watch(
    watch_id: int,
    data: WatchesUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить часы. Требуется админ."""
    service = WatchesService(database=db)
    watch = await service.update_watch(watch_id=watch_id, data=data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="watches",
        entity_id=watch_id,
        description=f"Обновлены часы {watch.name}",
        ip_address=request.client.host if request.client else None
    )
    
    return watch


@router.delete("/{watch_id}")
async def delete_watch(
    watch_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить часы. Требуется админ."""
    service = WatchesService(database=db)
    result = await service.delete_watch(watch_id=watch_id)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="watches",
        entity_id=watch_id,
        description=f"Удалены часы с ID {watch_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return result


@router.delete("/batch")
async def batch_delete_watches(
    request: Request,
    watch_ids: list[int] = Query(..., description="Список ID часов для удаления"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Массовое удаление часов. Требуется админ."""
    service = WatchesService(database=db)
    deleted_count = 0
    
    for wid in watch_ids:
        try:
            await service.delete_watch(watch_id=wid)
            deleted_count += 1
        except Exception as e:
            log.error(f"Не удалось удалить часы {wid}: {e}")
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="watches",
        description=f"Массовое удаление: удалено {deleted_count} из {len(watch_ids)} часов",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Удалено {deleted_count} из {len(watch_ids)} часов", "deleted_count": deleted_count}


@router.patch("/{watch_id}/count")
async def update_watch_count(
    watch_id: int,
    request: Request,
    count: int = Query(..., ge=0, description="Новое количество товара"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить количество товара на складе. Требуется админ."""
    from db.schemas.watches_schemas import WatchesUpdate
    service = WatchesService(database=db)
    watch = await service.update_watch(watch_id=watch_id, data=WatchesUpdate(count=count))
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="watches",
        entity_id=watch_id,
        description=f"Обновлено количество часов {watch.name}: {count} шт",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Количество обновлено на {count}", "watch_id": watch_id}
