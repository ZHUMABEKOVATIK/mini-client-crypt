from fastapi import APIRouter
from pydantic import BaseModel

from .price import router as price_router

routers = APIRouter(prefix="/api")
routers.include_router(price_router)
