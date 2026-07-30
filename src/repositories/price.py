from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.price import PriceTick

class PriceTickRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> PriceTick:
        new_data = PriceTick(**kwargs)
        self.session.add(new_data)
        await self.session.flush()
        return new_data

    async def get_all_by_ticker(self, ticker: str) -> list[PriceTick]:
        stmt = (
            select(PriceTick)
            .where(PriceTick.ticker == ticker)
            .order_by(PriceTick.timestamp)
        )

        result = (await self.session.scalars(stmt)).all()

        return result

    async def get_latest(self, ticker: str) -> PriceTick:
        stmt = (
            select(PriceTick)
            .where(PriceTick.ticker == ticker)
            .order_by(PriceTick.timestamp.desc())
            .limit(1)
        )

        return await self.session.scalar(stmt)

    async def get_by_date_range(self, ticker: str, date_from: datetime | None, date_to: datetime | None) -> list[PriceTick]:
        stmt = (
            select(PriceTick)
            .where(PriceTick.ticker == ticker)
        )

        if date_from:
            stmt = stmt.where(PriceTick.timestamp >= int(date_from.timestamp()))

        if date_to:
            stmt = stmt.where(PriceTick.timestamp <= int(date_to.timestamp()))

        stmt = stmt.order_by(PriceTick.timestamp)

        result = (
            await self.session.scalars(stmt)
        ).all()

        return result