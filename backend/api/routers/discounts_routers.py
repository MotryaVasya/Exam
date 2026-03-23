from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.discounts_services import DiscountsService
from db.schemas.discounts_schemas import DiscountsCreate, DiscountsInfo, DiscountsUpdate

router = APIRouter(prefix='/discounts', tags=['discounts'])


@router.post("/", response_model=DiscountsInfo)
async def create_discount(discount_data: DiscountsCreate, db: AsyncSession = Depends(get_db)):
    """Создать новую скидку."""
    service = DiscountsService(database=db)
    discount = await service.create_discount(data=discount_data)
    return discount


@router.get("/", response_model=list[DiscountsInfo])
async def get_all_discounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех скидок с пагинацией."""
    service = DiscountsService(database=db)
    discounts = await service.get_all_discounts(skip=skip, limit=limit)
    return discounts


@router.get("/{discount_id}", response_model=DiscountsInfo)
async def get_discount(discount_id: int, db: AsyncSession = Depends(get_db)):
    """Получить скидку по ID."""
    service = DiscountsService(database=db)
    discount = await service.get_discount(discount_id=discount_id)
    return discount


@router.get("/code/{discount_code}", response_model=DiscountsInfo | None)
async def get_discount_by_code(discount_code: str, db: AsyncSession = Depends(get_db)):
    """Получить скидку по коду."""
    service = DiscountsService(database=db)
    discount = await service.get_discount_by_code(discount_code=discount_code)
    return discount


@router.put("/{discount_id}", response_model=DiscountsInfo)
async def update_discount(
    discount_id: int, 
    data: DiscountsUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Обновить скидку."""
    service = DiscountsService(database=db)
    discount = await service.update_discount(discount_id=discount_id, data=data)
    return discount


@router.delete("/{discount_id}")
async def delete_discount(discount_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить скидку."""
    service = DiscountsService(database=db)
    result = await service.delete_discount(discount_id=discount_id)
    return result
