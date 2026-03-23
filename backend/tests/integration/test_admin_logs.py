"""
Интеграционные тесты для Admin Logs CRUD.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.admin_logs_crud import create, get, get_all, delete, delete_old_logs
from db.schemas.admin_logs_schemas import AdminLogsCreate


@pytest.mark.asyncio
class TestAdminLogsCRUD:
    """Тесты Admin Logs CRUD операций."""
    
    async def test_create_log(self, db_session: AsyncSession):
        """Тест создания лога."""
        log_data = AdminLogsCreate(
            admin_id=1,
            action="CREATE",
            entity="users",
            entity_id=1,
            description="Тестовый лог",
            ip_address="127.0.0.1"
        )
        
        log_entry = await create(db=db_session, data=log_data)
        
        assert log_entry.id is not None
        assert log_entry.action == "CREATE"
        assert log_entry.entity == "users"
        assert log_entry.admin_id == 1
    
    async def test_get_log(self, db_session: AsyncSession):
        """Тест получения лога по ID."""
        # Создаём лог
        log_data = AdminLogsCreate(
            admin_id=1,
            action="UPDATE",
            entity="watches",
            entity_id=5,
            description="Обновление часов",
            ip_address="127.0.0.1"
        )
        created_log = await create(db=db_session, data=log_data)
        
        # Получаем лог
        log_entry = await get(db=db_session, log_id=created_log.id)
        
        assert log_entry.id == created_log.id
        assert log_entry.action == "UPDATE"
    
    async def test_get_all_logs(self, db_session: AsyncSession):
        """Тест получения всех логов."""
        # Создаём несколько логов
        for i in range(5):
            log_data = AdminLogsCreate(
                admin_id=1,
                action="CREATE",
                entity="users",
                entity_id=i,
                description=f"Лог {i}"
            )
            await create(db=db_session, data=log_data)
        
        # Получаем все логи
        logs = await get_all(db=db_session, skip=0, limit=100)
        
        assert len(logs) == 5
    
    async def test_get_logs_filtered_by_action(self, db_session: AsyncSession):
        """Тест фильтрации логов по action."""
        # Создаём логи с разными action
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="CREATE", entity="users"))
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="DELETE", entity="users"))
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="CREATE", entity="watches"))
        
        # Фильтруем по CREATE
        logs = await get_all(db=db_session, skip=0, limit=100, action="CREATE")
        
        assert len(logs) == 2
    
    async def test_get_logs_filtered_by_entity(self, db_session: AsyncSession):
        """Тест фильтрации логов по entity."""
        # Создаём логи для разных сущностей
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="CREATE", entity="users"))
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="CREATE", entity="watches"))
        await create(db=db_session, data=AdminLogsCreate(admin_id=1, action="CREATE", entity="orders"))
        
        # Фильтруем по users
        logs = await get_all(db=db_session, skip=0, limit=100, entity="users")
        
        assert len(logs) == 1
    
    async def test_delete_log(self, db_session: AsyncSession):
        """Тест удаления лога."""
        # Создаём лог
        log_data = AdminLogsCreate(
            admin_id=1,
            action="TEST",
            entity="test",
            description="Лог для удаления"
        )
        created_log = await create(db=db_session, data=log_data)
        
        # Удаляем
        result = await delete(db=db_session, log_id=created_log.id)
        
        assert result is True
        
        # Проверяем что лог удалён
        from fastapi import HTTPException
        import pytest
        
        with pytest.raises(HTTPException):
            await get(db=db_session, log_id=created_log.id)
    
    async def test_delete_old_logs(self, db_session: AsyncSession):
        """Тест удаления старых логов."""
        from datetime import datetime, timedelta
        from sqlalchemy import update
        
        # Создаём лог
        log_data = AdminLogsCreate(
            admin_id=1,
            action="OLD",
            entity="test",
            description="Старый лог"
        )
        created_log = await create(db=db_session, data=log_data)
        
        # Искусственно "состариваем" лог (для теста)
        old_date = datetime.now() - timedelta(days=31)
        await db_session.execute(
            update(type(created_log))
            .where(type(created_log).id == created_log.id)
            .values(created_at=old_date)
        )
        await db_session.commit()
        
        # Удаляем старые логи
        count = await delete_old_logs(db=db_session, days=30)
        
        assert count >= 1
