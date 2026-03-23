import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Регистрация
user_data = {
    "first_name": "Тест",
    "last_name": "Тестов",
    "father_name": "Тестович",
    "email": "testjwt@example.com",
    "password": "password123",
    "is_active": False
}
print("1. Регистрация...")
resp = requests.post(f"{BASE_URL}/users/", json=user_data)
print(f"Status: {resp.status_code}")
user = resp.json()
user_id = user.get("id")
print(f"User ID: {user_id}")

# 2. Активация
print(f"\n2. Активация пользователя {user_id}...")
resp = requests.patch(f"{BASE_URL}/users/{user_id}?is_active=true")
print(f"Status: {resp.status_code}")

# 3. Логин
print("\n3. Логин...")
login_data = {"email": "testjwt@example.com", "password": "password123"}
resp = requests.post(f"{BASE_URL}/users/login", json=login_data)
print(f"Status: {resp.status_code}")
token_data = resp.json()
access_token = token_data.get("access_token")
print(f"Token: {access_token[:50]}...")

# 4. Тест токена вручную
print("\n4. Тест GET /users/me с токеном...")
headers = {"Authorization": f"Bearer {access_token}"}
print(f"Headers: {headers}")
resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")

# 5. Тест decode токена
print("\n5. Проверка токена через decode...")
from jose import jwt
try:
    payload = jwt.decode(access_token, "your-secret-key-change-in-production", algorithms=["HS256"])
    print(f"Payload: {payload}")
except Exception as e:
    print(f"Error: {e}")

# 6. Тест с другим endpoint
print("\n6. Тест POST /orders/ с токеном...")
order_data = {
    "user_id": user_id,
    "total_price": 1000.0,
    "is_pickup": True
}
resp = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
