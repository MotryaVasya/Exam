from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.watches_schemas import WatchesCreate, WatchesInfo, WatchesUpdate
from db.crud.watches_crud import create, get, get_all, update, delete
import logging

log = logging.getLogger(__name__)


class WatchesService:

    def __init__(self, database: AsyncSession):
        self.db = database

    async def create_watch(self, data: WatchesCreate) -> WatchesInfo:
        watch = await create(db=self.db, data=data)
        return WatchesInfo(
            id=watch.id,
            name=watch.name,
            producer_id=watch.producer_id,
            is_whatertightness=watch.is_whatertightness,
            released_at=watch.released_at,
            size_milimetrs=watch.size_milimetrs,
            type=watch.type,
            count=watch.count,
            gender=watch.gender,
            price=watch.price,
            image_url=watch.image_url,
            created_at=watch.created_at,
            updated_at=watch.updated_at
        )

    async def get_watch(self, watch_id: int) -> WatchesInfo:
        watch = await get(db=self.db, watch_id=watch_id)
        return WatchesInfo(
            id=watch.id,
            name=watch.name,
            producer_id=watch.producer_id,
            is_whatertightness=watch.is_whatertightness,
            released_at=watch.released_at,
            size_milimetrs=watch.size_milimetrs,
            type=watch.type,
            count=watch.count,
            gender=watch.gender,
            price=watch.price,
            image_url=watch.image_url,
            created_at=watch.created_at,
            updated_at=watch.updated_at
        )

    async def get_all_watches(
        self,
        skip: int = 0,
        limit: int = 100,
        producer_id: int | None = None,
        type: str | None = None,
        gender: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None
    ) -> list[WatchesInfo]:
        watches = await get_all(
            db=self.db,
            skip=skip,
            limit=limit,
            producer_id=producer_id,
            type=type,
            gender=gender,
            min_price=min_price,
            max_price=max_price
        )
        return [
            WatchesInfo(
                id=w.id,
                name=w.name,
                producer_id=w.producer_id,
                is_whatertightness=w.is_whatertightness,
                released_at=w.released_at,
                size_milimetrs=w.size_milimetrs,
                type=w.type,
                count=w.count,
                gender=w.gender,
                price=w.price,
                image_url=w.image_url,
                created_at=w.created_at,
                updated_at=w.updated_at
            ) for w in watches
        ]

    async def update_watch(self, watch_id: int, data: WatchesUpdate) -> WatchesInfo:
        watch = await update(db=self.db, watch_id=watch_id, data=data)
        return WatchesInfo(
            id=watch.id,
            name=watch.name,
            producer_id=watch.producer_id,
            is_whatertightness=watch.is_whatertightness,
            released_at=watch.released_at,
            size_milimetrs=watch.size_milimetrs,
            type=watch.type,
            count=watch.count,
            gender=watch.gender,
            price=watch.price,
            image_url=watch.image_url,
            created_at=watch.created_at,
            updated_at=watch.updated_at
        )

    async def delete_watch(self, watch_id: int) -> dict:
        result = await delete(db=self.db, watch_id=watch_id)
        return {"message": "Часы успешно удалены", "success": result}
