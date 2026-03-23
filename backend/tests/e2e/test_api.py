import requests
import json
from datetime import datetime, timedelta

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

# ==================== USERS ====================
print("\n" + "="*60)
print("👤 ТЕСТИРОВАНИЕ USERS")
print("="*60)

# 1. Регистрация пользователя
user_email = f"test{datetime.now().timestamp()}@example.com"
user_data = {
    "first_name": "Иван",
    "last_name": "Иванов",
    "father_name": "Иванович",
    "email": user_email,
    "password": "password123",
    "is_active": False
}
resp = print_response("POST /users/ - Регистрация", requests.post(f"{BASE_URL}/users/", json=user_data))
user = resp.json()
user_id = user.get("id")

# 2. Активация пользователя (через PATCH)
if user_id:
    resp = print_response(f"PATCH /users/{user_id} - Активация", requests.patch(f"{BASE_URL}/users/{user_id}?is_active=true"))

# 3. Логин
login_data = {"email": user_email, "password": "password123"}
resp = print_response("POST /users/login - Вход", requests.post(f"{BASE_URL}/users/login", json=login_data))
token_data = resp.json()
access_token = token_data.get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# 4. Получить текущего пользователя
if access_token:
    resp = print_response("GET /users/me - Текущий пользователь", requests.get(f"{BASE_URL}/users/me", headers=headers))

# 5. Получить пользователя по ID
if user_id:
    resp = print_response(f"GET /users/{user_id} - Пользователь по ID", requests.get(f"{BASE_URL}/users/{user_id}"))

# ==================== PRODUCERS ====================
print("\n" + "="*60)
print("🏭 ТЕСТИРОВАНИЕ PRODUCERS")
print("="*60)

# 1. Создать производителя
producer_data = {"name": "Rolex"}
resp = print_response("POST /producers/ - Создать производителя", requests.post(f"{BASE_URL}/producers/", json=producer_data))
producer = resp.json()
producer_id = producer.get("id")

# 2. Получить всех производителей
resp = print_response("GET /producers/ - Список производителей", requests.get(f"{BASE_URL}/producers/"))

# 3. Получить производителя по ID
if producer_id:
    resp = print_response(f"GET /producers/{producer_id} - Производитель по ID", requests.get(f"{BASE_URL}/producers/{producer_id}"))

# ==================== WATCHES ====================
print("\n" + "="*60)
print("⌚ ТЕСТИРОВАНИЕ WATCHES")
print("="*60)

# 1. Создать часы
from datetime import datetime, timedelta
watch_data = {
    "name": "Submariner",
    "producer_id": producer_id,
    "is_whatertightness": True,
    "released_at": (datetime.now() - timedelta(days=30)).isoformat(),
    "size_milimetrs": 40,
    "type": "mechanical",
    "count": 10,
    "gender": "male",
    "price": 500000.00
}
resp = print_response("POST /watches/ - Создать часы", requests.post(f"{BASE_URL}/watches/", json=watch_data))
watch = resp.json()
watch_id = watch.get("id")

# 2. Создать ещё часы для теста фильтрации
watch_data2 = {
    "name": "Speedmaster",
    "producer_id": producer_id,
    "is_whatertightness": False,
    "released_at": (datetime.now() - timedelta(days=60)).isoformat(),
    "size_milimetrs": 42,
    "type": "electronical",
    "count": 5,
    "gender": "unisex",
    "price": 300000.00
}
resp = print_response("POST /watches/ - Создать вторые часы", requests.post(f"{BASE_URL}/watches/", json=watch_data2))

# 3. Получить все часы с фильтрацией
resp = print_response("GET /watches/ - Все часы", requests.get(f"{BASE_URL}/watches/"))
resp = print_response("GET /watches/?type=mechanical - Фильтр по типу", requests.get(f"{BASE_URL}/watches/?type=mechanical"))
resp = print_response("GET /watches/?min_price=400000 - Фильтр по цене", requests.get(f"{BASE_URL}/watches/?min_price=400000"))

# 4. Получить часы по ID
if watch_id:
    resp = print_response(f"GET /watches/{watch_id} - Часы по ID", requests.get(f"{BASE_URL}/watches/{watch_id}"))

# ==================== DISCOUNTS ====================
print("\n" + "="*60)
print("💰 ТЕСТИРОВАНИЕ DISCOUNTS")
print("="*60)

# 1. Создать скидку
discount_data = {
    "discount_code": "SUMMER2024",
    "discount_percent": 15
}
resp = print_response("POST /discounts/ - Создать скидку", requests.post(f"{BASE_URL}/discounts/", json=discount_data))
discount = resp.json()
discount_id = discount.get("id")

# 2. Получить скидку по коду
resp = print_response("GET /discounts/code/SUMMER2024 - Скидка по коду", requests.get(f"{BASE_URL}/discounts/code/SUMMER2024"))

# 3. Получить все скидки
resp = print_response("GET /discounts/ - Список скидок", requests.get(f"{BASE_URL}/discounts/"))

# ==================== ORDERS ====================
print("\n" + "="*60)
print("📦 ТЕСТИРОВАНИЕ ORDERS")
print("="*60)

# 1. Создать заказ
order_data = {
    "user_id": user_id,
    "total_price": 500000.00,
    "discount": discount_id,
    "is_pickup": False,
    "delivery_address": "ул. Пушкина, д. 10"
}
resp = print_response("POST /orders/ - Создать заказ", requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers))
order = resp.json()
order_id = order.get("id")

# 2. Получить мои заказы
resp = print_response("GET /orders/my - Мои заказы", requests.get(f"{BASE_URL}/orders/my", headers=headers))

# 3. Получить количество заказов
resp = print_response("GET /orders/count/my - Количество заказов", requests.get(f"{BASE_URL}/orders/count/my", headers=headers))

# 4. Получить заказ по ID
if order_id:
    resp = print_response(f"GET /orders/{order_id} - Заказ по ID", requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers))

# ==================== ORDERS-WATCHES ====================
print("\n" + "="*60)
print("📦⌚ ТЕСТИРОВАНИЕ ORDERS-WATCHES")
print("="*60)

# 1. Добавить часы в заказ
order_watch_data = {
    "order_id": order_id,
    "watch_id": watch_id
}
resp = print_response("POST /orders-watches/ - Добавить часы в заказ", requests.post(f"{BASE_URL}/orders-watches/", json=order_watch_data, headers=headers))
order_watch = resp.json()
order_watch_id = order_watch.get("id")

# 2. Получить часы в заказе
resp = print_response(f"GET /orders-watches/order/{order_id} - Часы в заказе", requests.get(f"{BASE_URL}/orders-watches/order/{order_id}", headers=headers))

# 3. Получить все связи
resp = print_response("GET /orders-watches/ - Все связи", requests.get(f"{BASE_URL}/orders-watches/", headers=headers))

# ==================== VERIFICATION CODES ====================
print("\n" + "="*60)
print("📧 ТЕСТИРОВАНИЕ VERIFICATION CODES")
print("="*60)

# 1. Создать код верификации
resp = print_response(f"POST /verification-codes/?user_id={user_id} - Создать код", requests.post(f"{BASE_URL}/verification-codes/?user_id={user_id}", headers=headers))
verification_code = resp.json()
code_id = verification_code.get("id")
code_value = verification_code.get("code")

# 2. Получить код пользователя
resp = print_response(f"GET /verification-codes/user/{user_id} - Код пользователя", requests.get(f"{BASE_URL}/verification-codes/user/{user_id}", headers=headers))

# 3. Проверить код
resp = print_response(f"POST /verification-codes/verify?user_id={user_id}&code={code_value} - Проверка кода", 
                      requests.post(f"{BASE_URL}/verification-codes/verify?user_id={user_id}&code={code_value}"))

# ==================== UPDATE/DELETE ====================
print("\n" + "="*60)
print("✏️ ТЕСТИРОВАНИЕ UPDATE/DELETE")
print("="*60)

# 1. Обновить производителя
if producer_id:
    resp = print_response(f"PUT /producers/{producer_id} - Обновить производителя", 
                          requests.put(f"{BASE_URL}/producers/{producer_id}", json={"name": "Rolex SA"}, headers=headers))

# 2. Обновить часы
if watch_id:
    resp = print_response(f"PUT /watches/{watch_id} - Обновить часы", 
                          requests.put(f"{BASE_URL}/watches/{watch_id}", json={"price": 550000.00}, headers=headers))

# 3. Обновить заказ
if order_id:
    resp = print_response(f"PUT /orders/{order_id} - Обновить заказ", 
                          requests.put(f"{BASE_URL}/orders/{order_id}", json={"delivery_address": "ул. Ленина, д. 5"}, headers=headers))

# 4. Удалить связь заказа и часов
if order_watch_id:
    resp = print_response(f"DELETE /orders-watches/{order_watch_id} - Удалить связь", 
                          requests.delete(f"{BASE_URL}/orders-watches/{order_watch_id}", headers=headers))

# 5. Удалить заказ
if order_id:
    resp = print_response(f"DELETE /orders/{order_id} - Удалить заказ", 
                          requests.delete(f"{BASE_URL}/orders/{order_id}", headers=headers))

# 6. Удалить часы
if watch_id:
    resp = print_response(f"DELETE /watches/{watch_id} - Удалить часы", 
                          requests.delete(f"{BASE_URL}/watches/{watch_id}", headers=headers))

# 7. Удалить скидку
if discount_id:
    resp = print_response(f"DELETE /discounts/{discount_id} - Удалить скидку", 
                          requests.delete(f"{BASE_URL}/discounts/{discount_id}", headers=headers))

# 8. Удалить производителя
if producer_id:
    resp = print_response(f"DELETE /producers/{producer_id} - Удалить производителя", 
                          requests.delete(f"{BASE_URL}/producers/{producer_id}", headers=headers))

# 9. Удалить пользователя
if user_id:
    resp = print_response(f"DELETE /users/{user_id} - Удалить пользователя", 
                          requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers))

print("\n" + "="*60)
print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("="*60)
