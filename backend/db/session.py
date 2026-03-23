from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from core.config import settings
import logging

log = logging.getLogger(__name__)
async_engine = create_async_engine(settings.postgres_url, echo=True)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        log.info(
            msg="ВСЕ ТАБЛИЦЫ POSTGRESQL СОЗДАНЫ"
        )


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()