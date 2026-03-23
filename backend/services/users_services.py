from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.users_schemas import UsersCreate, UsersInfo, UsersUpdate, Token
from db.crud.users_crud import create, get, update, delete, login, update_status
import logging

log = logging.getLogger(__name__)
class UsersService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_user(self, data: UsersCreate) -> UsersInfo:
        user = await create(db=self.db, data=data)
        return UsersInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name or None,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )

    async def get_user(self, user_id: int) -> UsersInfo:
        user = await get(db=self.db, user_id=user_id)
        return UsersInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name or None,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )

    async def update_user(self, user_id: int, data: UsersUpdate) -> UsersInfo:
        user = await update(db=self.db, user_id=user_id, data=data)
        return UsersInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name or None,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )

    async def delete_user(self, user_id: int) -> dict:
        result = await delete(db=self.db, user_id=user_id)
        return {"message": "Пользователь успешно удалён", "success": result}

    async def udpate_status_user(self, user_id: int, status: bool = True) -> UsersInfo:
        user = await update_status(db=self.db, user_id=user_id, status=status)
        return UsersInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name or None,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin
        )

    async def login_user(self, email: str, password: str) -> Token:
        result = await login(db=self.db, email=email, password=password)
        return Token(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=UsersInfo(
                id=result["user"].id,
                first_name=result["user"].first_name,
                last_name=result["user"].last_name,
                father_name=result["user"].father_name or None,
                email=result["user"].email,
                is_active=result["user"].is_active,
                is_admin=result["user"].is_admin
            )
        )