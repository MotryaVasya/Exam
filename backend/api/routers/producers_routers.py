from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.producers_services import ProducersService
from db.schemas.producers_schemas import ProducersCreate, ProducersInfo, ProducersUpdate

router = APIRouter(prefix='/producers', tags=['producers'])


@router.post("/", response_model=ProducersInfo)
async def create_producer(producer_data: ProducersCreate, db: AsyncSession = Depends(get_db)):
    """Создать нового производителя."""
    service = ProducersService(database=db)
    producer = await service.create_producer(data=producer_data)
    return producer


@router.get("/", response_model=list[ProducersInfo])
async def get_all_producers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех производителей с пагинацией."""
    service = ProducersService(database=db)
    producers = await service.get_all_producers(skip=skip, limit=limit)
    return producers


@router.get("/{producer_id}", response_model=ProducersInfo)
async def get_producer(producer_id: int, db: AsyncSession = Depends(get_db)):
    """Получить производителя по ID."""
    service = ProducersService(database=db)
    producer = await service.get_producer(producer_id=producer_id)
    return producer


@router.put("/{producer_id}", response_model=ProducersInfo)
async def update_producer(
    producer_id: int, 
    data: ProducersUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Обновить производителя."""
    service = ProducersService(database=db)
    producer = await service.update_producer(producer_id=producer_id, data=data)
    return producer


@router.delete("/{producer_id}")
async def delete_producer(producer_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить производителя."""
    service = ProducersService(database=db)
    result = await service.delete_producer(producer_id=producer_id)
    return result
