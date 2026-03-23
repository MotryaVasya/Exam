from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.discounts_schemas import DiscountsCreate, DiscountsInfo, DiscountsUpdate
from db.crud.discounts_crud import create, get, get_by_code, get_all, update, delete
import logging

log = logging.getLogger(__name__)


class DiscountsService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_discount(self, data: DiscountsCreate) -> DiscountsInfo:
        discount = await create(db=self.db, data=data)
        return DiscountsInfo(
            id=discount.id,
            discount_code=discount.discount_code,
            discount_percent=discount.discount_percent
        )

    async def get_discount(self, discount_id: int) -> DiscountsInfo:
        discount = await get(db=self.db, discount_id=discount_id)
        return DiscountsInfo(
            id=discount.id,
            discount_code=discount.discount_code,
            discount_percent=discount.discount_percent
        )

    async def get_discount_by_code(self, discount_code: str) -> DiscountsInfo | None:
        discount = await get_by_code(db=self.db, discount_code=discount_code)
        if discount:
            return DiscountsInfo(
                id=discount.id,
                discount_code=discount.discount_code,
                discount_percent=discount.discount_percent
            )
        return None

    async def get_all_discounts(self, skip: int = 0, limit: int = 100) -> list[DiscountsInfo]:
        discounts = await get_all(db=self.db, skip=skip, limit=limit)
        return [
            DiscountsInfo(
                id=d.id,
                discount_code=d.discount_code,
                discount_percent=d.discount_percent
            ) for d in discounts
        ]

    async def update_discount(self, discount_id: int, data: DiscountsUpdate) -> DiscountsInfo:
        discount = await update(db=self.db, discount_id=discount_id, data=data)
        return DiscountsInfo(
            id=discount.id,
            discount_code=discount.discount_code,
            discount_percent=discount.discount_percent
        )

    async def delete_discount(self, discount_id: int) -> dict:
        result = await delete(db=self.db, discount_id=discount_id)
        return {"message": "Скидка успешно удалена", "success": result}
