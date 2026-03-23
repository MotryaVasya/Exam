"""
Конфигурация pytest и общие фикстуры для тестов.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db.session import get_db, Base
from db.models import Users
from core.config import settings


# URL тестовой базы данных (можно использовать test_ префикс)
TEST_DATABASE_URL = settings.postgres_url.replace(
    settings.POSTGRES_DB, 
    f"{settings.POSTGRES_DB}_test"
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Создаёт event loop для асинхронных тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """Создаёт тестовый движок SQLAlchemy."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        echo=False,
    )
    
    # Создаём все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Удаляем таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Создаёт сессию БД для тестов."""
    async_session = async_sessionmaker(
        test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создаёт тестовый HTTP клиент."""
    # Переопределяем зависимость get_db
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> dict:
    """Создаёт тестового администратора и возвращает данные для входа."""
    from core.config import context
    from datetime import datetime
    
    email = f"admin_{datetime.now().timestamp()}@test.com"
    hashed_password = context.hash("admin123456")
    
    admin = Users(
        first_name="Admin",
        last_name="Adminov",
        father_name="Adminovich",
        email=email,
        password=hashed_password,
        is_active=True,
        is_admin=True
    )
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    return {
        "id": admin.id,
        "email": email,
        "password": "admin123456"
    }


@pytest.fixture
async def regular_user(db_session: AsyncSession) -> dict:
    """Создаёт тестового пользователя и возвращает данные для входа."""
    from core.config import context
    from datetime import datetime
    
    email = f"user_{datetime.now().timestamp()}@test.com"
    hashed_password = context.hash("user123456")
    
    user = Users(
        first_name="Test",
        last_name="User",
        father_name=None,
        email=email,
        password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return {
        "id": user.id,
        "email": email,
        "password": "user123456"
    }


@pytest.fixture
async def admin_token(admin_user: dict, client: AsyncClient) -> str:
    """Возвращает JWT токен администратора."""
    response = await client.post(
        "/users/login",
        json={"email": admin_user["email"], "password": admin_user["password"]}
    )
    return response.json()["access_token"]


@pytest.fixture
async def user_token(regular_user: dict, client: AsyncClient) -> str:
    """Возвращает JWT токен обычного пользователя."""
    response = await client.post(
        "/users/login",
        json={"email": regular_user["email"], "password": regular_user["password"]}
    )
    return response.json()["access_token"]


# Хелперы для авторизации
def auth_headers(token: str) -> dict:
    """Возвращает заголовки для авторизованных запросов."""
    return {"Authorization": f"Bearer {token}"}
