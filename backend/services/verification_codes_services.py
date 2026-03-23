from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.verification_codes_schemas import VerificationCodesCreate, VerificationCodesInfo, VerificationCodesUpdate
from db.crud.verification_codes_crud import (
    create, get, get_by_user_id, verify_code, update, delete, delete_by_user_id, generate_code
)
import logging

log = logging.getLogger(__name__)


class VerificationCodesService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_verification_code(self, user_id: int, code: int | None = None) -> VerificationCodesInfo:
        data = VerificationCodesCreate(user_id=user_id, code=code if code else generate_code())
        verification_code = await create(db=self.db, data=data)
        return VerificationCodesInfo(
            id=verification_code.id,
            user_id=verification_code.user_id,
            code=verification_code.code,
            created_at=verification_code.created_at,
            updated_at=verification_code.updated_at
        )

    async def get_verification_code(self, code_id: int) -> VerificationCodesInfo:
        verification_code = await get(db=self.db, code_id=code_id)
        return VerificationCodesInfo(
            id=verification_code.id,
            user_id=verification_code.user_id,
            code=verification_code.code,
            created_at=verification_code.created_at,
            updated_at=verification_code.updated_at
        )

    async def get_verification_code_by_user_id(self, user_id: int) -> VerificationCodesInfo | None:
        verification_code = await get_by_user_id(db=self.db, user_id=user_id)
        if verification_code:
            return VerificationCodesInfo(
                id=verification_code.id,
                user_id=verification_code.user_id,
                code=verification_code.code,
                created_at=verification_code.created_at,
                updated_at=verification_code.updated_at
            )
        return None

    async def verify_user_code(self, user_id: int, code: int) -> bool:
        return await verify_code(db=self.db, user_id=user_id, code=code)

    async def update_verification_code(self, code_id: int, data: VerificationCodesUpdate) -> VerificationCodesInfo:
        verification_code = await update(db=self.db, code_id=code_id, data=data)
        return VerificationCodesInfo(
            id=verification_code.id,
            user_id=verification_code.user_id,
            code=verification_code.code,
            created_at=verification_code.created_at,
            updated_at=verification_code.updated_at
        )

    async def delete_verification_code(self, code_id: int) -> dict:
        result = await delete(db=self.db, code_id=code_id)
        return {"message": "Код верификации успешно удалён", "success": result}

    async def delete_verification_codes_by_user_id(self, user_id: int) -> dict:
        result = await delete_by_user_id(db=self.db, user_id=user_id)
        return {"message": "Все коды верификации пользователя успешно удалены", "success": result}
