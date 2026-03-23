from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.discounts_services import DiscountsService
from services.admin_logs_services import log_admin_action
from db.schemas.discounts_schemas import DiscountsCreate, DiscountsInfo, DiscountsUpdate
from core.jwt import get_current_admin_user
from db.models import Users
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/discounts', tags=['admin_discounts'])


@router.get("/", response_model=list[DiscountsInfo])
async def get_all_discounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список всех скидок с пагинацией. Требуется админ."""
    service = DiscountsService(database=db)
    return await service.get_all_discounts(skip=skip, limit=limit)


@router.get("/{discount_id}", response_model=DiscountsInfo)
async def get_discount(
    discount_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить скидку по ID. Требуется админ."""
    service = DiscountsService(database=db)
    discount = await service.get_discount(discount_id=discount_id)
    return discount


@router.post("/", response_model=DiscountsInfo)
async def create_discount(
    discount_data: DiscountsCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Создать новую скидку. Требуется админ."""
    service = DiscountsService(database=db)
    discount = await service.create_discount(data=discount_data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="CREATE",
        entity="discounts",
        entity_id=discount.id,
        description=f"Создана скидка {discount.discount_code} ({discount.discount_percent}%)",
        ip_address=request.client.host if request.client else None
    )
    
    return discount


@router.put("/{discount_id}", response_model=DiscountsInfo)
async def update_discount(
    discount_id: int,
    data: DiscountsUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить скидку. Требуется админ."""
    service = DiscountsService(database=db)
    discount = await service.update_discount(discount_id=discount_id, data=data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="discounts",
        entity_id=discount_id,
        description=f"Обновлена скидка {discount.discount_code}",
        ip_address=request.client.host if request.client else None
    )
    
    return discount


@router.delete("/{discount_id}")
async def delete_discount(
    discount_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить скидку. Требуется админ."""
    service = DiscountsService(database=db)
    result = await service.delete_discount(discount_id=discount_id)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="discounts",
        entity_id=discount_id,
        description=f"Удалена скидка с ID {discount_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return result


@router.delete("/batch")
async def batch_delete_discounts(
    request: Request,
    discount_ids: list[int] = Query(..., description="Список ID скидок для удаления"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Массовое удаление скидок. Требуется админ."""
    service = DiscountsService(database=db)
    deleted_count = 0
    
    for did in discount_ids:
        try:
            await service.delete_discount(discount_id=did)
            deleted_count += 1
        except Exception as e:
            log.error(f"Не удалось удалить скидку {did}: {e}")
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="discounts",
        description=f"Массовое удаление: удалено {deleted_count} из {len(discount_ids)} скидок",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Удалено {deleted_count} из {len(discount_ids)} скидок", "deleted_count": deleted_count}
