from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sessions import get_async_session
from typing import Annotated
from fastapi import Depends

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]