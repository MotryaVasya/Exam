from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.users_schemas import UsersCreate, UsersInfo
from db.session import get_db
from services.users_services import UsersService


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/", response_model=UsersInfo)
async def post(user_data: UsersCreate, db: AsyncSession = Depends(get_db)):
    service = UsersService(db)
    try:
        user = await service.create_user(data=user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        pass

@router.get('/{user_id}')
async def get():
    pass

@router.put('/{user_id}')
async def put():
    pass