from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.verification_codes_services import VerificationCodesService
from db.schemas.verification_codes_schemas import (
    VerificationCodesCreate, 
    VerificationCodesInfo, 
    VerificationCodesUpdate
)
from core.jwt import get_current_user
from db.schemas.users_schemas import UsersInfo

router = APIRouter(prefix='/verification-codes', tags=['verification_codes'])


@router.post("/", response_model=VerificationCodesInfo)
async def create_verification_code(
    user_id: int = Query(..., description="ID пользователя для которого создаётся код"),
    code: int | None = Query(None, description="Код верификации (если не указан, будет сгенерирован автоматически)"),
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Создать код верификации для пользователя. Требуется авторизация."""
    service = VerificationCodesService(database=db)
    verification_code = await service.create_verification_code(user_id=user_id, code=code)
    return verification_code


@router.get("/{code_id}", response_model=VerificationCodesInfo)
async def get_verification_code(code_id: int, db: AsyncSession = Depends(get_db)):
    """Получить код верификации по ID."""
    service = VerificationCodesService(database=db)
    verification_code = await service.get_verification_code(code_id=code_id)
    return verification_code


@router.get("/user/{user_id}", response_model=VerificationCodesInfo | None)
async def get_verification_code_by_user_id(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Получить последний код верификации пользователя. Требуется авторизация."""
    service = VerificationCodesService(database=db)
    verification_code = await service.get_verification_code_by_user_id(user_id=user_id)
    return verification_code


@router.post("/verify", response_model=dict)
async def verify_code(
    user_id: int = Query(..., description="ID пользователя"),
    code: int = Query(..., description="Код верификации"),
    db: AsyncSession = Depends(get_db)
):
    """Проверить код верификации."""
    service = VerificationCodesService(database=db)
    is_valid = await service.verify_user_code(user_id=user_id, code=code)
    if is_valid:
        return {"message": "Код верификации успешно подтверждён", "success": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код верификации"
        )


@router.put("/{code_id}", response_model=VerificationCodesInfo)
async def update_verification_code(
    code_id: int, 
    data: VerificationCodesUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить код верификации."""
    service = VerificationCodesService(database=db)
    verification_code = await service.update_verification_code(code_id=code_id, data=data)
    return verification_code


@router.delete("/{code_id}")
async def delete_verification_code(
    code_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Удалить код верификации."""
    service = VerificationCodesService(database=db)
    result = await service.delete_verification_code(code_id=code_id)
    return result


@router.delete("/user/{user_id}")
async def delete_verification_codes_by_user_id(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UsersInfo = Depends(get_current_user)
):
    """Удалить все коды верификации пользователя. Требуется авторизация."""
    service = VerificationCodesService(database=db)
    result = await service.delete_verification_codes_by_user_id(user_id=user_id)
    return result
