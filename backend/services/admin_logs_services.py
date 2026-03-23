from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.admin_logs_schemas import AdminLogsCreate, AdminLogsInfo
from db.crud.admin_logs_crud import create, get, get_all, delete, delete_old_logs
import logging

log = logging.getLogger(__name__)


class AdminLogsService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_log(self, data: AdminLogsCreate) -> AdminLogsInfo:
        log_entry = await create(db=self.db, data=data)
        return AdminLogsInfo(
            id=log_entry.id,
            admin_id=log_entry.admin_id,
            action=log_entry.action,
            entity=log_entry.entity,
            entity_id=log_entry.entity_id,
            description=log_entry.description,
            ip_address=log_entry.ip_address,
            created_at=log_entry.created_at
        )

    async def get_log(self, log_id: int) -> AdminLogsInfo:
        log_entry = await get(db=self.db, log_id=log_id)
        return AdminLogsInfo(
            id=log_entry.id,
            admin_id=log_entry.admin_id,
            action=log_entry.action,
            entity=log_entry.entity,
            entity_id=log_entry.entity_id,
            description=log_entry.description,
            ip_address=log_entry.ip_address,
            created_at=log_entry.created_at
        )

    async def get_all_logs(
        self, 
        skip: int = 0, 
        limit: int = 100,
        admin_id: int | None = None,
        action: str | None = None,
        entity: str | None = None
    ) -> list[AdminLogsInfo]:
        logs = await get_all(
            db=self.db, 
            skip=skip, 
            limit=limit,
            admin_id=admin_id,
            action=action,
            entity=entity
        )
        return [
            AdminLogsInfo(
                id=l.id,
                admin_id=l.admin_id,
                action=l.action,
                entity=l.entity,
                entity_id=l.entity_id,
                description=l.description,
                ip_address=l.ip_address,
                created_at=l.created_at
            ) for l in logs
        ]

    async def delete_log(self, log_id: int) -> dict:
        result = await delete(db=self.db, log_id=log_id)
        return {"message": "Лог успешно удалён", "success": result}

    async def delete_old_logs(self, days: int = 30) -> dict:
        count = await delete_old_logs(db=self.db, days=days)
        return {"message": f"Удалено {count} старых логов", "deleted_count": count}


async def log_admin_action(
    db: AsyncSession,
    admin_id: int,
    action: str,
    entity: str,
    entity_id: int | None = None,
    description: str | None = None,
    ip_address: str | None = None
) -> AdminLogsInfo:
    """Быстрая функция для логирования действий админа."""
    service = AdminLogsService(database=db)
    data = AdminLogsCreate(
        admin_id=admin_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description,
        ip_address=ip_address
    )
    return await service.create_log(data=data)
