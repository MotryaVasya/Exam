from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.admin_logs_services import AdminLogsService
from db.schemas.admin_logs_schemas import AdminLogsInfo
from core.jwt import get_current_admin_user
from db.models import Users
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/logs', tags=['admin_logs'])


@router.get("/", response_model=list[AdminLogsInfo])
async def get_all_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin_id: int | None = Query(None),
    action: str | None = Query(None),
    entity: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список логов действий админа с фильтрацией и пагинацией. Требуется админ."""
    service = AdminLogsService(database=db)
    return await service.get_all_logs(
        skip=skip,
        limit=limit,
        admin_id=admin_id,
        action=action,
        entity=entity
    )


@router.get("/{log_id}", response_model=AdminLogsInfo)
async def get_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить лог по ID. Требуется админ."""
    service = AdminLogsService(database=db)
    log_entry = await service.get_log(log_id=log_id)
    return log_entry


@router.delete("/{log_id}")
async def delete_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить лог. Требуется админ."""
    service = AdminLogsService(database=db)
    result = await service.delete_log(log_id=log_id)
    return result


@router.post("/cleanup")
async def cleanup_old_logs(
    days: int = Query(30, ge=1, le=365, description="Удалить логи старше N дней"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить старые логи. Требуется админ."""
    service = AdminLogsService(database=db)
    result = await service.delete_old_logs(days=days)
    return result
