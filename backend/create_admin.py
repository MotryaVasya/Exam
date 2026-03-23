"""
Скрипт для создания первого администратора.
Запуск: python create_admin.py
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from db.models import Users
from core.config import context

# Настройки подключения (должны совпадать с .env)
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "exam"

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


async def create_admin():
    print("=" * 60)
    print("🔐 Создание администратора")
    print("=" * 60)
    
    # Ввод данных
    print("\nВведите данные для создания администратора:")
    first_name = input("Имя: ").strip()
    last_name = input("Фамилия: ").strip()
    father_name = input("Отчество (необязательно): ").strip() or None
    email = input("Email: ").strip()
    password = input("Пароль (минимум 8 символов): ").strip()
    
    if len(password) < 8:
        print("❌ Пароль должен быть минимум 8 символов!")
        return
    
    # Подключение к БД
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Проверка существующего пользователя
        check = await db.execute(select(Users).where(Users.email == email))
        if check.scalar_one_or_none():
            print(f"❌ Пользователь с email {email} уже существует!")
            return
        
        # Хэширование пароля
        hashed_password = context.hash(password)
        
        # Создание админа
        admin = Users(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            email=email,
            password=hashed_password,
            is_active=True,
            is_admin=True
        )
        
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        
        print("\n" + "=" * 60)
        print("✅ Администратор успешно создан!")
        print("=" * 60)
        print(f"\nID: {admin.id}")
        print(f"Email: {admin.email}")
        print(f"Роль: Администратор (is_admin=True)")
        print("\nТеперь вы можете войти через POST /users/login")
        print("И использовать токен для доступа к /admin/* endpoint'ам")
        print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(create_admin())
    except KeyboardInterrupt:
        print("\n\nОтменено пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nУбедитесь что:")
        print("1. База данных запущена")
        print("2. Параметры подключения верные")
        print("3. Таблицы созданы (запустите main.py хотя бы один раз)")
        sys.exit(1)
