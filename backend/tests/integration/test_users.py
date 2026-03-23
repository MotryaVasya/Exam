"""
Интеграционные тесты для Users CRUD.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Users
from db.crud.users_crud import create, get, update, delete, update_status, veify_password
from db.schemas.users_schemas import UsersCreate, UsersUpdate
from core.config import context


@pytest.mark.asyncio
class TestUsersCRUD:
    """Тесты Users CRUD операций."""
    
    async def test_create_user(self, db_session: AsyncSession):
        """Тест создания пользователя."""
        user_data = UsersCreate(
            first_name="Test",
            last_name="User",
            father_name="Testovich",
            email="test@example.com",
            password="password123",
            is_active=True,
            is_admin=False
        )
        
        user = await create(db=db_session, data=user_data)
        
        assert user.id is not None
        assert user.first_name == "Test"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_admin is False
    
    async def test_create_user_duplicate_email(self, db_session: AsyncSession):
        """Тест создания пользователя с дублирующимся email."""
        from fastapi import HTTPException
        
        user_data = UsersCreate(
            first_name="Test",
            last_name="User",
            father_name=None,
            email="duplicate@example.com",
            password="password123",
            is_active=True
        )
        
        # Создаём первого пользователя
        await create(db=db_session, data=user_data)
        
        # Пытаемся создать второго с тем же email
        with pytest.raises(HTTPException) as exc_info:
            await create(db=db_session, data=user_data)
        
        assert exc_info.value.status_code == 409
    
    async def test_create_user_short_password(self, db_session: AsyncSession):
        """Тест создания пользователя с коротким паролем."""
        from fastapi import HTTPException
        
        user_data = UsersCreate(
            first_name="Test",
            last_name="User",
            father_name=None,
            email="short@example.com",
            password="123",  # Слишком короткий
            is_active=True
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await create(db=db_session, data=user_data)
        
        assert exc_info.value.status_code == 400
    
    async def test_get_user(self, db_session: AsyncSession):
        """Тест получения пользователя по ID."""
        # Создаём пользователя
        user_data = UsersCreate(
            first_name="Get",
            last_name="Test",
            father_name=None,
            email="get@example.com",
            password="password123",
            is_active=True
        )
        created_user = await create(db=db_session, data=user_data)
        
        # Получаем пользователя
        user = await get(db=db_session, user_id=created_user.id)
        
        assert user.id == created_user.id
        assert user.email == "get@example.com"
    
    async def test_get_nonexistent_user(self, db_session: AsyncSession):
        """Тест получения несуществующего пользователя."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            await get(db=db_session, user_id=99999)
        
        assert exc_info.value.status_code == 404
    
    async def test_update_user(self, db_session: AsyncSession):
        """Тест обновления пользователя."""
        # Создаём пользователя
        user_data = UsersCreate(
            first_name="Update",
            last_name="Test",
            father_name=None,
            email="update@example.com",
            password="password123",
            is_active=True
        )
        created_user = await create(db=db_session, data=user_data)
        
        # Обновляем
        update_data = UsersUpdate(first_name="Updated")
        updated_user = await update(db=db_session, user_id=created_user.id, data=update_data)
        
        assert updated_user.first_name == "Updated"
        assert updated_user.email == "update@example.com"
    
    async def test_update_user_password(self, db_session: AsyncSession):
        """Тест обновления пароля пользователя."""
        # Создаём пользователя
        user_data = UsersCreate(
            first_name="Password",
            last_name="Test",
            father_name=None,
            email="password@example.com",
            password="old_password123",
            is_active=True
        )
        created_user = await create(db=db_session, data=user_data)
        
        # Обновляем пароль
        update_data = UsersUpdate(password="new_password123")
        updated_user = await update(db=db_session, user_id=created_user.id, data=update_data)
        
        # Проверяем что пароль обновился (сравниваем хэши)
        assert updated_user.password != created_user.password
    
    async def test_delete_user(self, db_session: AsyncSession):
        """Тест удаления пользователя."""
        # Создаём пользователя
        user_data = UsersCreate(
            first_name="Delete",
            last_name="Test",
            father_name=None,
            email="delete@example.com",
            password="password123",
            is_active=True
        )
        created_user = await create(db=db_session, data=user_data)
        
        # Удаляем
        result = await delete(db=db_session, user_id=created_user.id)
        
        assert result is True
        
        # Проверяем что пользователь удалён
        res = await db_session.execute(select(Users).where(Users.id == created_user.id))
        deleted_user = res.scalar_one_or_none()
        assert deleted_user is None
    
    async def test_update_status(self, db_session: AsyncSession):
        """Тест обновления статуса пользователя."""
        # Создаём пользователя
        user_data = UsersCreate(
            first_name="Status",
            last_name="Test",
            father_name=None,
            email="status@example.com",
            password="password123",
            is_active=True
        )
        created_user = await create(db=db_session, data=user_data)
        
        # Деактивируем
        updated_user = await update_status(db=db_session, user_id=created_user.id, status=False)
        
        assert updated_user.is_active is False
        
        # Активируем обратно
        updated_user = await update_status(db=db_session, user_id=created_user.id, status=True)
        
        assert updated_user.is_active is True
    
    async def test_password_hashing(self, db_session: AsyncSession):
        """Тест хэширования пароля."""
        user_data = UsersCreate(
            first_name="Hash",
            last_name="Test",
            father_name=None,
            email="hash@example.com",
            password="test_password123",
            is_active=True
        )
        
        user = await create(db=db_session, data=user_data)
        
        # Проверяем что пароль захэширован
        assert user.password != "test_password123"
        assert len(user.password) > 50  # Argon2 хэш достаточно длинный
        
        # Проверяем валидацию пароля
        is_valid = await veify_password("test_password123", user.password)
        assert is_valid is True
        
        # Проверяем неверный пароль
        is_invalid = await veify_password("wrong_password", user.password)
        assert is_invalid is False
