from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.users_schemas import UsersCreate, UsersInfo
from db.crud.users_crud import create, get, update, delete, login

class UsersService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_user(self, data: UsersCreate) -> UsersInfo:
        try:
            user = await create(db=self.db, data=data)
            return UsersInfo(
                first_name=user.first_name,
                last_name=user.last_name,
                father_name=user.father_name,
                email=user.email,
                is_active=user.is_active
            )
        except Exception as e:
            print(str(e))