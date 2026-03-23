# API Документация

## Описание

Backend API для приложения Exam (интернет-магазин часов).

## Структура проекта

```
backend/
├── api/
│   └── routers/          # HTTP роутеры (endpoints)
│       ├── admin_*.py    # Админ-панель
│       └── *.py          # Публичные роутеры
├── core/
│   ├── config.py         # Конфигурация приложения
│   └── jwt.py            # JWT утилиты
├── db/
│   ├── crud/             # CRUD операции для каждой модели
│   ├── schemas/          # Pydantic схемы
│   ├── models.py         # SQLAlchemy модели
│   └── session.py        # Подключение к БД
├── services/             # Бизнес-логика
├── main.py               # Точка входа
└── .env                  # Переменные окружения
```

## Авторизация

### Роли пользователей

- **Обычный пользователь** (`is_admin=False`) — доступ к базовым endpoint'ам
- **Администратор** (`is_admin=True`) — доступ ко всем endpoint'ам включая админ-панель

### Получение токена

```bash
POST /users/login
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "is_admin": true
  }
}
```

### Использование токена

```
Authorization: Bearer <your_token>
```

---

## 🔐 Админ-панель

Все endpoint'ы админ-панели требуют `is_admin=true` в токене.

### Admin Users (Управление пользователями)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/users/` | Список пользователей (пагинация + фильтры) |
| GET | `/admin/users/count` | Общее количество пользователей |
| GET | `/admin/users/{user_id}` | Пользователь по ID |
| POST | `/admin/users/` | Создать пользователя |
| PUT | `/admin/users/{user_id}` | Обновить пользователя |
| PATCH | `/admin/users/{user_id}/status?is_active=true` | Изменить статус |
| DELETE | `/admin/users/{user_id}` | Удалить пользователя |
| DELETE | `/admin/users/batch?user_ids=1&user_ids=2` | Массовое удаление |

**Параметры для GET /admin/users/:**
- `skip`, `limit` — пагинация
- `is_active` — фильтр по статусу
- `is_admin` — фильтр по роли
- `search` — поиск по email/имени

---

### Admin Producers (Управление производителями)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/producers/` | Список (пагинация + поиск) |
| GET | `/admin/producers/{producer_id}` | По ID |
| POST | `/admin/producers/` | Создать |
| PUT | `/admin/producers/{producer_id}` | Обновить |
| DELETE | `/admin/producers/{producer_id}` | Удалить |
| DELETE | `/admin/producers/batch?producer_ids=1&producer_ids=2` | Массовое удаление |

---

### Admin Watches (Управление товарами)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/watches/` | Список (пагинация + фильтры) |
| GET | `/admin/watches/{watch_id}` | По ID |
| POST | `/admin/watches/` | Создать |
| PUT | `/admin/watches/{watch_id}` | Обновить |
| DELETE | `/admin/watches/{watch_id}` | Удалить |
| DELETE | `/admin/watches/batch?watch_ids=1&watch_ids=2` | Массовое удаление |
| PATCH | `/admin/watches/{watch_id}/count?count=50` | Обновить количество |

**Параметры для GET /admin/watches/:**
- `skip`, `limit` — пагинация
- `producer_id`, `type`, `gender` — фильтры
- `min_price`, `max_price` — диапазон цен
- `search` — поиск по названию

---

### Admin Orders (Управление заказами)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/orders/` | Список (пагинация + фильтры) |
| GET | `/admin/orders/count` | Общее количество |
| GET | `/admin/orders/{order_id}` | По ID |
| POST | `/admin/orders/` | Создать |
| PUT | `/admin/orders/{order_id}` | Обновить |
| DELETE | `/admin/orders/{order_id}` | Удалить |
| DELETE | `/admin/orders/batch?order_ids=1&order_ids=2` | Массовое удаление |

---

### Admin Discounts (Управление скидками)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/discounts/` | Список (пагинация) |
| GET | `/admin/discounts/{discount_id}` | По ID |
| POST | `/admin/discounts/` | Создать |
| PUT | `/admin/discounts/{discount_id}` | Обновить |
| DELETE | `/admin/discounts/{discount_id}` | Удалить |
| DELETE | `/admin/discounts/batch?discount_ids=1&discount_ids=2` | Массовое удаление |

---

### Admin Logs (Логи действий админа)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/logs/` | Список логов (пагинация + фильтры) |
| GET | `/admin/logs/{log_id}` | Лог по ID |
| DELETE | `/admin/logs/{log_id}` | Удалить лог |
| POST | `/admin/logs/cleanup?days=30` | Удалить логи старше N дней |

**Параметры для GET /admin/logs/:**
- `skip`, `limit` — пагинация
- `admin_id` — фильтр по админу
- `action` — тип действия (CREATE, UPDATE, DELETE)
- `entity` — сущность (users, watches, orders...)

---

### Admin Stats (Статистика)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/admin/stats/` | Общая статистика |
| GET | `/admin/stats/revenue?period=week` | Выручка за период |
| GET | `/admin/stats/top-products?limit=10` | Топ популярных товаров |

**Пример ответа /admin/stats/:**
```json
{
  "users": { "total": 100, "active": 85, "admins": 3 },
  "orders": { "total": 250, "total_revenue": 1250000, "average_order_price": 5000 },
  "watches": { "total_products": 50, "total_in_stock": 500 },
  "producers": { "total": 10 },
  "discounts": { "total": 5 }
}
```

**Параметры для /admin/stats/revenue:**
- `period` — `all`, `today`, `week`, `month`

---

## Публичные API

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/producers/` | Создать производителя | ❌ |
| GET | `/producers/` | Список всех производителей (пагинация) | ❌ |
| GET | `/producers/{producer_id}` | Получить производителя по ID | ❌ |
| PUT | `/producers/{producer_id}` | Обновить производителя | ❌ |
| DELETE | `/producers/{producer_id}` | Удалить производителя | ❌ |

**Query параметры для GET /producers/:**
- `skip` (int, default=0) - пропустить N записей
- `limit` (int, default=100) - количество записей

---

### ⌚ Watches (Часы)

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/watches/` | Создать часы | ❌ |
| GET | `/watches/` | Список всех часов (фильтрация + пагинация) | ❌ |
| GET | `/watches/{watch_id}` | Получить часы по ID | ❌ |
| PUT | `/watches/{watch_id}` | Обновить часы | ❌ |
| DELETE | `/watches/{watch_id}` | Удалить часы | ❌ |

**Query параметры для GET /watches/:**
- `skip` (int, default=0)
- `limit` (int, default=100)
- `producer_id` (int, optional) - фильтр по производителю
- `type` (str, optional) - тип: `electronical`, `mechanical`, `hybrid`
- `gender` (str, optional) - пол: `unisex`, `male`, `female`
- `min_price` (float, optional) - минимальная цена
- `max_price` (float, optional) - максимальная цена

**Пример создания:**
```json
POST /watches/
{
  "name": "Speedster Pro",
  "producer_id": 1,
  "is_whatertightness": true,
  "released_at": "2024-01-15T00:00:00",
  "size_milimetrs": 42,
  "type": "mechanical",
  "count": 50,
  "gender": "male",
  "price": 25000.00
}
```

---

### 📧 Verification Codes (Коды верификации)

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/verification-codes/` | Создать код верификации | ✅ |
| GET | `/verification-codes/{code_id}` | Получить код по ID | ❌ |
| GET | `/verification-codes/user/{user_id}` | Получить код пользователя | ✅ |
| POST | `/verification-codes/verify` | Проверить код | ❌ |
| PUT | `/verification-codes/{code_id}` | Обновить код | ❌ |
| DELETE | `/verification-codes/{code_id}` | Удалить код | ❌ |
| DELETE | `/verification-codes/user/{user_id}` | Удалить все коды пользователя | ✅ |

**Query параметры для POST /verification-codes/:**
- `user_id` (int) - ID пользователя
- `code` (int, optional) - код (если не указан, генерируется автоматически)

**Пример проверки:**
```
POST /verification-codes/verify?user_id=1&code=123456
```

---

### 💰 Discounts (Скидки)

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/discounts/` | Создать скидку | ❌ |
| GET | `/discounts/` | Список всех скидок (пагинация) | ❌ |
| GET | `/discounts/{discount_id}` | Получить скидку по ID | ❌ |
| GET | `/discounts/code/{discount_code}` | Получить скидку по коду | ❌ |
| PUT | `/discounts/{discount_id}` | Обновить скидку | ❌ |
| DELETE | `/discounts/{discount_id}` | Удалить скидку | ❌ |

**Пример создания:**
```json
POST /discounts/
{
  "discount_code": "SUMMER2024",
  "discount_percent": 15
}
```

---

### 📦 Orders (Заказы)

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/orders/` | Создать заказ | ✅ |
| GET | `/orders/` | Список всех заказов | ✅ |
| GET | `/orders/my` | Мои заказы | ✅ |
| GET | `/orders/{order_id}` | Получить заказ по ID | ✅ |
| PUT | `/orders/{order_id}` | Обновить заказ | ✅ |
| DELETE | `/orders/{order_id}` | Удалить заказ | ✅ |
| GET | `/orders/count/my` | Количество моих заказов | ✅ |

**Пример создания:**
```json
POST /orders/
{
  "user_id": 1,
  "total_price": 25000.00,
  "discount": 1,
  "is_pickup": false,
  "delivery_address": "ул. Пушкина, д. 10"
}
```

---

### 📦⌚ Orders-Watches (Связь заказов и часов)

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | `/orders-watches/` | Добавить часы в заказ | ✅ |
| GET | `/orders-watches/` | Список всех связей | ✅ |
| GET | `/orders-watches/order/{order_id}` | Часы в заказе | ✅ |
| GET | `/orders-watches/{id}` | Получить связь по ID | ✅ |
| PUT | `/orders-watches/{id}` | Обновить связь | ✅ |
| DELETE | `/orders-watches/{id}` | Удалить связь | ✅ |
| DELETE | `/orders-watches/order/{order_id}` | Удалить все связи заказа | ✅ |

**Пример создания:**
```json
POST /orders-watches/
{
  "order_id": 1,
  "watch_id": 5
}
```

---

## Авторизация

Для доступа к защищённым endpoint'ам необходимо передавать JWT токен в заголовке:

```
Authorization: Bearer <your_token>
```

## Запуск сервера

```bash
cd backend
.venv\Scripts\activate
python main.py
```

Сервер запустится на `http://localhost:8000`

## Swagger документация

После запуска сервера доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
