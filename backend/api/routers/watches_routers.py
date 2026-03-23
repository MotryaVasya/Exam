from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.watches_services import WatchesService
from db.schemas.watches_schemas import WatchesCreate, WatchesInfo, WatchesUpdate
from datetime import datetime

router = APIRouter(prefix='/watches', tags=['watches'])


@router.post("/", response_model=WatchesInfo)
async def create_watch(watch_data: WatchesCreate, db: AsyncSession = Depends(get_db)):
    """Создать новые часы."""
    service = WatchesService(database=db)
    watch = await service.create_watch(data=watch_data)
    return watch


@router.get("/", response_model=list[WatchesInfo])
async def get_all_watches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    producer_id: int | None = Query(None, description="Фильтр по производителю"),
    type: str | None = Query(None, description="Фильтр по типу (electronical, mechanical, hybrid)"),
    gender: str | None = Query(None, description="Фильтр по полу (unisex, male, female)"),
    min_price: float | None = Query(None, ge=0, description="Минимальная цена"),
    max_price: float | None = Query(None, ge=0, description="Максимальная цена"),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех часов с фильтрацией и пагинацией."""
    service = WatchesService(database=db)
    watches = await service.get_all_watches(
        skip=skip, 
        limit=limit,
        producer_id=producer_id,
        type=type,
        gender=gender,
        min_price=min_price,
        max_price=max_price
    )
    return watches


@router.get("/{watch_id}", response_model=WatchesInfo)
async def get_watch(watch_id: int, db: AsyncSession = Depends(get_db)):
    """Получить часы по ID."""
    service = WatchesService(database=db)
    watch = await service.get_watch(watch_id=watch_id)
    return watch


@router.put("/{watch_id}", response_model=WatchesInfo)
async def update_watch(
    watch_id: int, 
    data: WatchesUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Обновить часы."""
    service = WatchesService(database=db)
    watch = await service.update_watch(watch_id=watch_id, data=data)
    return watch


@router.delete("/{watch_id}")
async def delete_watch(watch_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить часы."""
    service = WatchesService(database=db)
    result = await service.delete_watch(watch_id=watch_id)
    return result
