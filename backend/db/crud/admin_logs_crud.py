from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from db.models import AdminLogs
from db.schemas.admin_logs_schemas import AdminLogsCreate, AdminLogsUpdate
from datetime import datetime
import logging

log = logging.getLogger(__name__)


async def create(db: AsyncSession, data: AdminLogsCreate) -> AdminLogs:
    try:
        log_entry = AdminLogs(
            admin_id=data.admin_id,
            action=data.action,
            entity=data.entity,
            entity_id=data.entity_id,
            description=data.description,
            ip_address=data.ip_address
        )
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при создании лога админа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании лога: {str(e)}"
        )


async def get(db: AsyncSession, log_id: int) -> AdminLogs:
    if log_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID лога невозможен!"
        )
    try:
        res = await db.execute(select(AdminLogs).where(AdminLogs.id == log_id))
        log_entry = res.scalar_one_or_none()
        if not log_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого лога не существует!"
            )
        return log_entry
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Ошибка при получении лога: {e}, log_id: {log_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении лога: {str(e)}"
        )


async def get_all(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    admin_id: int | None = None,
    action: str | None = None,
    entity: str | None = None
) -> list[AdminLogs]:
    try:
        query = select(AdminLogs).order_by(desc(AdminLogs.created_at))
        
        if admin_id:
            query = query.where(AdminLogs.admin_id == admin_id)
        if action:
            query = query.where(AdminLogs.action == action)
        if entity:
            query = query.where(AdminLogs.entity == entity)
        
        query = query.offset(skip).limit(limit)
        res = await db.execute(query)
        logs = res.scalars().all()
        return logs
    except Exception as e:
        log.error(f"Ошибка при получении списка логов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка логов: {str(e)}"
        )


async def delete(db: AsyncSession, log_id: int) -> bool:
    if log_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой ID лога невозможен!"
        )
    try:
        res = await db.execute(select(AdminLogs).where(AdminLogs.id == log_id))
        log_entry = res.scalar_one_or_none()

        if not log_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого лога не существует!"
            )
        await db.delete(log_entry)
        await db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении лога с ID {log_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении лога: {str(e)}"
        )


async def delete_old_logs(db: AsyncSession, days: int = 30) -> int:
    """Удаляет логи старше указанного количества дней."""
    try:
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        res = await db.execute(
            select(AdminLogs).where(AdminLogs.created_at < cutoff_date)
        )
        old_logs = res.scalars().all()
        count = len(old_logs)
        
        for log_entry in old_logs:
            await db.delete(log_entry)
        
        await db.commit()
        log.info(f"Удалено {count} старых логов")
        return count
    except Exception as e:
        await db.rollback()
        log.error(f"Ошибка при удалении старых логов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении старых логов: {str(e)}"
        )
