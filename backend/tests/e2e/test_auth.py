"""
E2E тесты для авторизации и прав доступа.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuth:
    """Тесты авторизации и JWT токенов."""
    
    async def test_admin_login_returns_token(self, client: AsyncClient, admin_user: dict):
        """Тест входа администратора."""
        response = await client.post(
            "/users/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["is_admin"] is True
    
    async def test_user_login_returns_token(self, client: AsyncClient, regular_user: dict):
        """Тест входа обычного пользователя."""
        response = await client.post(
            "/users/login",
            json={
                "email": regular_user["email"],
                "password": regular_user["password"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["user"]["is_admin"] is False
    
    async def test_login_wrong_password(self, client: AsyncClient, admin_user: dict):
        """Тест входа с неверным паролем."""
        response = await client.post(
            "/users/login",
            json={
                "email": admin_user["email"],
                "password": "wrong_password"
            }
        )
        
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Тест входа несуществующего пользователя."""
        response = await client.post(
            "/users/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401


@pytest.mark.asyncio
class TestAdminAccess:
    """Тесты доступа к админ-панели."""
    
    async def test_admin_can_access_admin_stats(self, client: AsyncClient, admin_token: str):
        """Тест доступа администратора к статистике."""
        response = await client.get(
            "/admin/stats/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "users" in data
        assert "orders" in data
        assert "watches" in data
    
    async def test_user_cannot_access_admin_stats(self, client: AsyncClient, user_token: str):
        """Тест запрета доступа обычного пользователя к статистике."""
        response = await client.get(
            "/admin/stats/",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 403
    
    async def test_unauthorized_cannot_access_admin(self, client: AsyncClient):
        """Тест запрета доступа без авторизации."""
        response = await client.get("/admin/stats/")
        
        assert response.status_code == 401
    
    async def test_admin_can_access_admin_users(self, client: AsyncClient, admin_token: str):
        """Тест доступа администратора к пользователям."""
        response = await client.get(
            "/admin/users/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_user_cannot_access_admin_users(self, client: AsyncClient, user_token: str):
        """Тест запрета доступа обычного пользователя к управлению пользователями."""
        response = await client.get(
            "/admin/users/",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 403
    
    async def test_admin_can_access_admin_logs(self, client: AsyncClient, admin_token: str):
        """Тест доступа администратора к логам."""
        response = await client.get(
            "/admin/logs/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_user_cannot_access_admin_logs(self, client: AsyncClient, user_token: str):
        """Тест запрета доступа обычного пользователя к логам."""
        response = await client.get(
            "/admin/logs/",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 403


@pytest.mark.asyncio
class TestUserAccess:
    """Тесты доступа обычного пользователя."""
    
    async def test_user_can_access_own_profile(self, client: AsyncClient, user_token: str):
        """Тест доступа пользователя к своему профилю."""
        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "email" in data
        assert "is_admin" in data
        assert data["is_admin"] is False
    
    async def test_user_can_access_own_orders(self, client: AsyncClient, user_token: str):
        """Тест доступа пользователя к своим заказам."""
        response = await client.get(
            "/orders/my",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_unauthorized_cannot_access_profile(self, client: AsyncClient):
        """Тест запрета доступа к профилю без авторизации."""
        response = await client.get("/users/me")
        
        assert response.status_code == 401
