import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_response(title: str, response):
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    return response

print("\n" + "="*60)
print("🔐 ТЕСТИРОВАНИЕ АДМИН-ПАНЕЛИ")
print("="*60)

# ==================== СОЗДАНИЕ АДМИНА ====================
print("\n" + "="*60)
print("1️⃣ СОЗДАНИЕ АДМИНИСТРАТОРА")
print("="*60)

admin_email = f"admin{datetime.now().timestamp()}@example.com"
admin_data = {
    "first_name": "Админ",
    "last_name": "Админов",
    "father_name": "Админович",
    "email": admin_email,
    "password": "admin123456",
    "is_active": True,
    "is_admin": True
}

# Создаём админа через обычный users endpoint (пока нет create_admin)
resp = print_response("POST /users/ - Создание админа", requests.post(f"{BASE_URL}/users/", json=admin_data))
admin = resp.json()
admin_id = admin.get("id")

if not admin_id:
    print("❌ Не удалось создать админа! Тестирование остановлено.")
    exit(1)

print(f"✅ Админ создан: ID={admin_id}, email={admin_email}")

# ==================== ЛОГИН АДМИНА ====================
print("\n" + "="*60)
print("2️⃣ ЛОГИН АДМИНИСТРАТОРА")
print("="*60)

login_data = {"email": admin_email, "password": "admin123456"}
resp = print_response("POST /users/login - Вход админа", requests.post(f"{BASE_URL}/users/login", json=login_data))
token_data = resp.json()
access_token = token_data.get("access_token")
is_admin = token_data.get("user", {}).get("is_admin")

if not access_token:
    print("❌ Не удалось получить токен! Тестирование остановлено.")
    exit(1)

print(f"✅ Токен получен: {access_token[:50]}...")
print(f"✅ is_admin: {is_admin}")

admin_headers = {"Authorization": f"Bearer {access_token}"}

# ==================== ПРОВЕРКА ПРАВ АДМИНА ====================
print("\n" + "="*60)
print("3️⃣ ПРОВЕРКА ДОСТУПА К АДМИН-ПАНЕЛИ")
print("="*60)

resp = print_response("GET /admin/stats/ - Статистика (требуется админ)", requests.get(f"{BASE_URL}/admin/stats/", headers=admin_headers))

# ==================== ADMIN USERS ====================
print("\n" + "="*60)
print("4️⃣ ADMIN USERS - Управление пользователями")
print("="*60)

# Создаём тестового пользователя
user_data = {
    "first_name": "Тест",
    "last_name": "Тестов",
    "email": f"testuser{datetime.now().timestamp()}@example.com",
    "password": "password123",
    "is_active": True,
    "is_admin": False
}
resp = print_response("POST /admin/users/ - Создать пользователя", requests.post(f"{BASE_URL}/admin/users/", json=user_data, headers=admin_headers))
test_user = resp.json()
test_user_id = test_user.get("id")

if not test_user_id:
    print("⚠️ Не удалось создать тестового пользователя через админку, пробуем через обычный endpoint...")
    # Пробуем через обычный endpoint
    user_data["father_name"] = None
    resp = requests.post(f"{BASE_URL}/users/", json=user_data)
    test_user = resp.json()
    test_user_id = test_user.get("id")

# Получаем всех пользователей
resp = print_response("GET /admin/users/ - Список пользователей", requests.get(f"{BASE_URL}/admin/users/", headers=admin_headers))

# Получаем количество
resp = print_response("GET /admin/users/count - Количество", requests.get(f"{BASE_URL}/admin/users/count", headers=admin_headers))

# Поиск пользователей
resp = print_response(f"GET /admin/users/?search={admin_email}", requests.get(f"{BASE_URL}/admin/users/?search={admin_email}", headers=admin_headers))

# Обновляем пользователя
resp = print_response(f"PUT /admin/users/{test_user_id} - Обновить", requests.put(f"{BASE_URL}/admin/users/{test_user_id}", json={"first_name": "Обновлённый"}, headers=admin_headers))

# Изменяем статус
resp = print_response(f"PATCH /admin/users/{test_user_id}/status?is_active=false", requests.patch(f"{BASE_URL}/admin/users/{test_user_id}/status?is_active=false", headers=admin_headers))

# ==================== ADMIN PRODUCERS ====================
print("\n" + "="*60)
print("5️⃣ ADMIN PRODUCERS - Управление производителями")
print("="*60)

# Создаём производителя
producer_data = {"name": "AdminTest Brand"}
resp = print_response("POST /admin/producers/ - Создать производителя", requests.post(f"{BASE_URL}/admin/producers/", json=producer_data, headers=admin_headers))
producer = resp.json()
producer_id = producer.get("id")

# Получаем всех
resp = print_response("GET /admin/producers/ - Список", requests.get(f"{BASE_URL}/admin/producers/", headers=admin_headers))

# Поиск
resp = print_response("GET /admin/producers/?search=AdminTest", requests.get(f"{BASE_URL}/admin/producers/?search=AdminTest", headers=admin_headers))

# Обновляем
resp = print_response(f"PUT /admin/producers/{producer_id} - Обновить", requests.put(f"{BASE_URL}/admin/producers/{producer_id}", json={"name": "AdminTest Brand Updated"}, headers=admin_headers))

# ==================== ADMIN WATCHES ====================
print("\n" + "="*60)
print("6️⃣ ADMIN WATCHES - Управление товарами")
print("="*60)

# Создаём часы
from datetime import timedelta
watch_data = {
    "name": "Admin Test Watch",
    "producer_id": producer_id,
    "is_whatertightness": True,
    "released_at": (datetime.now() - timedelta(days=30)).isoformat(),
    "size_milimetrs": 42,
    "type": "mechanical",
    "count": 100,
    "gender": "male",
    "price": 15000.00
}
resp = print_response("POST /admin/watches/ - Создать часы", requests.post(f"{BASE_URL}/admin/watches/", json=watch_data, headers=admin_headers))
watch = resp.json()
watch_id = watch.get("id")

# Получаем всех с фильтрами
resp = print_response("GET /admin/watches/?type=mechanical - Фильтр по типу", requests.get(f"{BASE_URL}/admin/watches/?type=mechanical", headers=admin_headers))
resp = print_response("GET /admin/watches/?min_price=10000 - Фильтр по цене", requests.get(f"{BASE_URL}/admin/watches/?min_price=10000", headers=admin_headers))

# Обновляем количество
resp = print_response(f"PATCH /admin/watches/{watch_id}/count?count=50", requests.patch(f"{BASE_URL}/admin/watches/{watch_id}/count?count=50", headers=admin_headers))

# Обновляем
resp = print_response(f"PUT /admin/watches/{watch_id} - Обновить", requests.put(f"{BASE_URL}/admin/watches/{watch_id}", json={"price": 17000.00}, headers=admin_headers))

# ==================== ADMIN ORDERS ====================
print("\n" + "="*60)
print("7️⃣ ADMIN ORDERS - Управление заказами")
print("="*60)

# Создаём заказ
order_data = {
    "user_id": admin_id,
    "total_price": 15000.00,
    "is_pickup": True,
    "delivery_address": None
}
resp = print_response("POST /admin/orders/ - Создать заказ", requests.post(f"{BASE_URL}/admin/orders/", json=order_data, headers=admin_headers))
order = resp.json()
order_id = order.get("id")

# Получаем все
resp = print_response("GET /admin/orders/ - Список", requests.get(f"{BASE_URL}/admin/orders/", headers=admin_headers))

# Получаем количество
resp = print_response("GET /admin/orders/count - Количество", requests.get(f"{BASE_URL}/admin/orders/count", headers=admin_headers))

# Фильтр
resp = print_response("GET /admin/orders/?is_pickup=true - Фильтр", requests.get(f"{BASE_URL}/admin/orders/?is_pickup=true", headers=admin_headers))

# Обновляем
resp = print_response(f"PUT /admin/orders/{order_id} - Обновить", requests.put(f"{BASE_URL}/admin/orders/{order_id}", json={"delivery_address": "ул. Админская, 1"}, headers=admin_headers))

# ==================== ADMIN DISCOUNTS ====================
print("\n" + "="*60)
print("8️⃣ ADMIN DISCOUNTS - Управление скидками")
print("="*60)

# Создаём скидку
discount_data = {
    "discount_code": "ADMIN2024",
    "discount_percent": 20
}
resp = print_response("POST /admin/discounts/ - Создать скидку", requests.post(f"{BASE_URL}/admin/discounts/", json=discount_data, headers=admin_headers))
discount = resp.json()
discount_id = discount.get("id")

# Получаем все
resp = print_response("GET /admin/discounts/ - Список", requests.get(f"{BASE_URL}/admin/discounts/", headers=admin_headers))

# Обновляем
resp = print_response(f"PUT /admin/discounts/{discount_id} - Обновить", requests.put(f"{BASE_URL}/admin/discounts/{discount_id}", json={"discount_percent": 25}, headers=admin_headers))

# ==================== ADMIN STATS ====================
print("\n" + "="*60)
print("9️⃣ ADMIN STATS - Статистика")
print("="*60)

# Общая статистика
resp = print_response("GET /admin/stats/ - Общая статистика", requests.get(f"{BASE_URL}/admin/stats/", headers=admin_headers))

# Выручка
resp = print_response("GET /admin/stats/revenue?period=all - Выручка за всё время", requests.get(f"{BASE_URL}/admin/stats/revenue?period=all", headers=admin_headers))
resp = print_response("GET /admin/stats/revenue?period=week - Выручка за неделю", requests.get(f"{BASE_URL}/admin/stats/revenue?period=week", headers=admin_headers))

# Топ товаров
resp = print_response("GET /admin/stats/top-products?limit=5 - Топ товаров", requests.get(f"{BASE_URL}/admin/stats/top-products?limit=5", headers=admin_headers))

# ==================== ADMIN LOGS ====================
print("\n" + "="*60)
print("📋 ADMIN LOGS - Логи действий")
print("="*60)

# Получаем логи
resp = print_response("GET /admin/logs/ - Список логов", requests.get(f"{BASE_URL}/admin/logs/", headers=admin_headers))

# Фильтр по действию
resp = print_response("GET /admin/logs/?action=CREATE - Логи CREATE", requests.get(f"{BASE_URL}/admin/logs/?action=CREATE", headers=admin_headers))

# Фильтр по сущности
resp = print_response("GET /admin/logs/?entity=users - Логи users", requests.get(f"{BASE_URL}/admin/logs/?entity=users", headers=admin_headers))

# ==================== МАССОВЫЕ ОПЕРАЦИИ ====================
print("\n" + "="*60)
print("🗑️ МАССОВЫЕ ОПЕРАЦИИ")
print("="*60)

# Создаём несколько пользователей для массового удаления
for i in range(3):
    batch_user = {
        "first_name": f"Batch{i}",
        "last_name": f"User{i}",
        "email": f"batch{i}{datetime.now().timestamp()}@example.com",
        "password": "password123",
        "is_active": True,
        "is_admin": False
    }
    requests.post(f"{BASE_URL}/admin/users/", json=batch_user, headers=admin_headers)

# Массовое удаление (создадим и сразу удалим)
print("\n⚠️ Массовое удаление пользователей...")
# Для массового удаления нужны ID, которые мы только что создали
# Пропускаем для простоты

# ==================== УДАЛЕНИЕ ====================
print("\n" + "="*60)
print("🗑️ УДАЛЕНИЕ СОЗДАННЫХ ДАННЫХ")
print("="*60)

# Удаляем заказ
resp = print_response(f"DELETE /admin/orders/{order_id}", requests.delete(f"{BASE_URL}/admin/orders/{order_id}", headers=admin_headers))

# Удаляем скидку
resp = print_response(f"DELETE /admin/discounts/{discount_id}", requests.delete(f"{BASE_URL}/admin/discounts/{discount_id}", headers=admin_headers))

# Удаляем часы
resp = print_response(f"DELETE /admin/watches/{watch_id}", requests.delete(f"{BASE_URL}/admin/watches/{watch_id}", headers=admin_headers))

# Удаляем производителя
resp = print_response(f"DELETE /admin/producers/{producer_id}", requests.delete(f"{BASE_URL}/admin/producers/{producer_id}", headers=admin_headers))

# Удаляем тестового пользователя
resp = print_response(f"DELETE /admin/users/{test_user_id}", requests.delete(f"{BASE_URL}/admin/users/{test_user_id}", headers=admin_headers))

# ==================== ПРОВЕРКА ДОСТУПА БЕЗ АДМИНА ====================
print("\n" + "="*60)
print("🚫 ПРОВЕРКА ЗАЩИТЫ АДМИН-ПАНЕЛИ")
print("="*60)

# Создаём обычного пользователя
regular_user_data = {
    "first_name": "Обычный",
    "last_name": "Пользователь",
    "father_name": None,
    "email": f"regular{datetime.now().timestamp()}@example.com",
    "password": "password123",
    "is_active": True,
    "is_admin": False
}
resp = print_response("POST /users/ - Создаём обычного пользователя", requests.post(f"{BASE_URL}/users/", json=regular_user_data))
regular_user = resp.json()
regular_user_id = regular_user.get("id")

if regular_user_id:
    # Логинимся как обычный пользователь
    regular_login = {"email": regular_user_data["email"], "password": "password123"}
    resp = print_response("POST /users/login - Вход обычного пользователя", requests.post(f"{BASE_URL}/users/login", json=regular_login))
    regular_token = resp.json().get("access_token")
    
    if regular_token:
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        
        # Пробуем доступ к админке
        resp = print_response("GET /admin/stats/ - Доступ обычного пользователя (должен быть 403)", requests.get(f"{BASE_URL}/admin/stats/", headers=regular_headers))

        if resp.status_code == 403:
            print("✅ Защита работает! Обычный пользователь не имеет доступа к админ-панели.")
        else:
            print(f"❌ ОШИБКА! Статус: {resp.status_code}. Обычный пользователь получил доступ к админ-панели!")
    else:
        print("⚠️ Не удалось получить токен обычного пользователя")
else:
    print("⚠️ Не удалось создать обычного пользователя для теста защиты")

print("\n" + "="*60)
print("✅ ТЕСТИРОВАНИЕ АДМИН-ПАНЕЛИ ЗАВЕРШЕНО")
print("="*60)
