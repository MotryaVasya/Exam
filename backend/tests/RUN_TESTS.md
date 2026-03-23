# Тестирование API

## Структура тестов

```
tests/
├── unit/                    # Юнит-тесты
│   └── test_jwt.py          # Тесты JWT утилит
├── integration/             # Интеграционные тесты
│   ├── test_users.py        # Тесты Users CRUD
│   └── test_admin_logs.py   # Тесты Admin Logs CRUD
└── e2e/                     # End-to-End тесты
    ├── test_api.py          # Полное тестирование API
    ├── test_admin.py        # Тестирование админ-панели
    ├── test_auth.py         # Тесты авторизации
    └── test_jwt_e2e.py      # E2E тесты JWT
```

## Установка зависимостей

```bash
cd backend
.venv\Scripts\activate
.venv\Scripts\pip install pytest pytest-asyncio pytest-cov httpx
```

## Запуск тестов

### Все тесты
```bash
python -m pytest tests/ -v
```

### Только unit-тесты
```bash
python -m pytest tests/unit/ -v
```

### Только интеграционные тесты
```bash
python -m pytest tests/integration/ -v
```

### Только e2e тесты
```bash
python -m pytest tests/e2e/ -v
```

### Отдельный тест
```bash
python -m pytest tests/unit/test_jwt.py -v
python -m pytest tests/e2e/test_auth.py -v
```

### Отдельная тест-функция
```bash
python -m pytest tests/unit/test_jwt.py::TestCreateAccessToken::test_create_token_with_sub -v
```

### Тесты с покрытием (coverage)
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

Отчёт откроется в `htmlcov/index.html`

### Тесты с выводом логов
```bash
python -m pytest tests/ -v -s
```

### Тесты с остановкой на первой ошибке
```bash
python -m pytest tests/ -x
```

## Типы тестов

### Unit тесты (`tests/unit/`)
- Тестируют отдельные функции/классы
- Без подключения к БД
- Быстрые, изолированные

### Интеграционные тесты (`tests/integration/`)
- Тестируют взаимодействие компонентов
- CRUD операции с БД
- Сервисы

### E2E тесты (`tests/e2e/`)
- Полные сценарии через HTTP
- Тестируют всё приложение целиком
- Требуют запущенного сервера или используют test client

## Фикстуры

В `conftest.py` определены общие фикстуры:

- `client` - HTTP клиент для тестов
- `db_session` - сессия БД для тестов
- `admin_user` - тестовый администратор
- `regular_user` - тестовый пользователь
- `admin_token` - JWT токен администратора
- `user_token` - JWT токен пользователя

## Пример написания теста

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_admin_can_access_stats(client: AsyncClient, admin_token: str):
    """Администратор может получить статистику."""
    response = await client.get(
        "/admin/stats/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
```

## CI/CD

Для интеграции с CI/CD:

```bash
# Запуск с junit отчётом
python -m pytest tests/ --junitxml=test-results.xml

# Запуск с coverage в формате cobertura
python -m pytest tests/ --cov=. --cov-report=xml:cobertura.xml
```
