"""
Юнит-тесты для JWT утилит.
"""
import pytest
from datetime import datetime, timedelta
from core.jwt import create_access_token, decode_access_token
from core.config import settings


class TestCreateAccessToken:
    """Тесты функции создания токена."""
    
    def test_create_token_with_sub(self):
        """Тест создания токена с sub."""
        token = create_access_token(data={"sub": "123"})
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_token_with_int_sub(self):
        """Тест создания токена с int sub (должен конвертироваться в строку)."""
        token = create_access_token(data={"sub": 123})
        assert token is not None
        
        payload = decode_access_token(token)
        assert payload["sub"] == "123"
    
    def test_create_token_with_is_admin(self):
        """Тест создания токена с is_admin."""
        token = create_access_token(data={"sub": "1"}, is_admin=True)
        payload = decode_access_token(token)
        assert payload["is_admin"] is True
    
    def test_create_token_without_is_admin(self):
        """Тест создания токена без is_admin (по умолчанию False)."""
        token = create_access_token(data={"sub": "1"})
        payload = decode_access_token(token)
        assert payload["is_admin"] is False
    
    def test_create_token_with_custom_expiry(self):
        """Тест создания токена с custom временем жизни."""
        custom_delta = timedelta(hours=2)
        token = create_access_token(data={"sub": "1"}, expires_delta=custom_delta)
        payload = decode_access_token(token)
        assert payload["exp"] is not None


class TestDecodeAccessToken:
    """Тесты функции декодирования токена."""
    
    def test_decode_valid_token(self):
        """Тест декодирования валидного токена."""
        token = create_access_token(data={"sub": "test_user"}, is_admin=True)
        payload = decode_access_token(token)
        
        assert payload["sub"] == "test_user"
        assert payload["is_admin"] is True
    
    def test_decode_invalid_token(self):
        """Тест декодирования невалидного токена."""
        invalid_token = "invalid.token.here"
        payload = decode_access_token(invalid_token)
        assert payload is None
    
    def test_decode_expired_token(self):
        """Тест декодирования истёкшего токена."""
        # Создаём токен с отрицательным временем жизни
        token = create_access_token(
            data={"sub": "1"}, 
            expires_delta=timedelta(seconds=-1)
        )
        payload = decode_access_token(token)
        # Токен с истёкшим сроком должен возвращать None
        assert payload is None
    
    def test_decode_token_missing_exp(self):
        """Тест токена без exp (должен работать)."""
        from jose import jwt
        from datetime import datetime
        
        to_encode = {"sub": "1", "is_admin": True}
        token = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        payload = decode_access_token(token)
        assert payload["sub"] == "1"
        assert payload["is_admin"] is True


class TestTokenPayload:
    """Тесты структуры payload токена."""
    
    def test_token_has_required_claims(self):
        """Тест наличия обязательных claims."""
        token = create_access_token(data={"sub": "123"}, is_admin=True)
        payload = decode_access_token(token)
        
        assert "sub" in payload
        assert "exp" in payload
        assert "is_admin" in payload
    
    def test_sub_is_string(self):
        """Тест что sub всегда строка."""
        token = create_access_token(data={"sub": 42})
        payload = decode_access_token(token)
        assert isinstance(payload["sub"], str)
        assert payload["sub"] == "42"
