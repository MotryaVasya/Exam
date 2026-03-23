# Tests Directory

## Структура

```
tests/
├── __init__.py
├── conftest.py              # Общие фикстуры для pytest
├── unit/                    # Юнит-тесты (отдельные функции)
│   ├── __init__.py
│   ├── test_jwt.py          # Тесты JWT утилит
│   └── test_schemas.py      # Тесты схем
├── integration/             # Интеграционные тесты (CRUD, Services)
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_producers.py
│   ├── test_watches.py
│   ├── test_orders.py
│   ├── test_discounts.py
│   └── test_admin_logs.py
└── e2e/                     # End-to-End тесты (полные сценарии)
    ├── __init__.py
    ├── test_api.py          # Тестирование всех API endpoint'ов
    ├── test_admin.py        # Тестирование админ-панели
    └── test_auth.py         # Тесты авторизации и прав доступа
```

## Запуск тестов

### Все тесты
```bash
cd backend
.venv\Scripts\python -m pytest tests/ -v
```

### Только юнит-тесты
```bash
.venv\Scripts\python -m pytest tests/unit/ -v
```

### Только интеграционные
```bash
.venv\Scripts\python -m pytest tests/integration/ -v
```

### Только e2e
```bash
.venv\Scripts\python -m pytest tests/e2e/ -v
```

### Тесты с покрытием
```bash
.venv\Scripts\python -m pytest tests/ --cov=backend --cov-report=html
```

### Отдельный тест
```bash
.venv\Scripts\python -m pytest tests/e2e/test_admin.py -v
```

## Зависимости для тестов

```bash
.venv\Scripts\pip install pytest pytest-asyncio pytest-cov httpx
```

## Структура тестов

### Unit тесты
Тестируют отдельные функции без подключения к БД:
- JWT генерация/валидация
- Валидация схем Pydantic
- Хэширование паролей

### Integration тесты
Тестируют работу с БД:
- CRUD операции
- Сервисы
- Валидация данных

### E2E тесты
Тестируют полные сценарии через HTTP:
- Регистрация → Логин → Получение данных
- Админ-панель: создание → редактирование → удаление
- Проверка прав доступа
