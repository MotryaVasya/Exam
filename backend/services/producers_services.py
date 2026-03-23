from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.producers_schemas import ProducersCreate, ProducersInfo, ProducersUpdate
from db.crud.producers_crud import create, get, get_all, update, delete
import logging

log = logging.getLogger(__name__)


class ProducersService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_producer(self, data: ProducersCreate) -> ProducersInfo:
        producer = await create(db=self.db, data=data)
        return ProducersInfo(
            id=producer.id,
            name=producer.name,
            created_at=producer.created_at,
            updated_at=producer.updated_at
        )

    async def get_producer(self, producer_id: int) -> ProducersInfo:
        producer = await get(db=self.db, producer_id=producer_id)
        return ProducersInfo(
            id=producer.id,
            name=producer.name,
            created_at=producer.created_at,
            updated_at=producer.updated_at
        )

    async def get_all_producers(self, skip: int = 0, limit: int = 100) -> list[ProducersInfo]:
        producers = await get_all(db=self.db, skip=skip, limit=limit)
        return [
            ProducersInfo(
                id=p.id,
                name=p.name,
                created_at=p.created_at,
                updated_at=p.updated_at
            ) for p in producers
        ]

    async def update_producer(self, producer_id: int, data: ProducersUpdate) -> ProducersInfo:
        producer = await update(db=self.db, producer_id=producer_id, data=data)
        return ProducersInfo(
            id=producer.id,
            name=producer.name,
            created_at=producer.created_at,
            updated_at=producer.updated_at
        )

    async def delete_producer(self, producer_id: int) -> dict:
        result = await delete(db=self.db, producer_id=producer_id)
        return {"message": "Производитель успешно удалён", "success": result}
