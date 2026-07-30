from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

# ================================= Async Session Zone =================================
async_engine = create_async_engine(settings.DB_URL_ASYNC)

async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session