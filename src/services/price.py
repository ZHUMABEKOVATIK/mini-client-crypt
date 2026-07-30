from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.price import PriceTick
from src.repositories.price import PriceTickRepository

class PriceService:
    def __init__(self, session: AsyncSession):
        self.repo = PriceTickRepository(session)

    async def create(self, ticker: str, price: float, timestamp: int) -> PriceTick:
        data = await self.repo.create(
            ticker = ticker,
            price = price,
            timestamp = timestamp
        )
        return data

    async def get_all_by_ticker(self, ticker: str) -> list[PriceTick]:
        return await self.repo.get_all_by_ticker(ticker)

    async def get_latest(self, ticker: str) -> PriceTick:
        return await self.repo.get_latest(ticker)

    async def get_by_date_range(self, ticker: str, date_from: datetime | None, date_to: datetime | None) -> list[PriceTick]:
        return await self.repo.get_by_date_range(
            ticker = ticker, 
            date_from = date_from, 
            date_to = date_to
        )