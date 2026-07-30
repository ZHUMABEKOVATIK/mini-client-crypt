from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.models import *
from src.database.base import Base
from src.database.sessions import async_engine

@asynccontextmanager
async def life_span(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Start")
    
    yield

    await async_engine.dispose()
    print("End")