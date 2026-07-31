import asyncio
import time

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.utils.logger_config import logger
from src.core.celery_app import celery_app
from src.database.sessions import async_session
from src.services.deribit_client import DeribitClient
from src.services.price import PriceService
from src.core.config import settings

async def fetch_prices() -> int:
    now = int(time.time())
    client = DeribitClient()
    saved = 0

    engine = create_async_engine(settings.DB_URL_ASYNC, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        price_service = PriceService(session)
        for ticker in ["btc_usd", "eth_usd"]:
            try:
                resp = await client.get_index_price(ticker)
                await price_service.create(
                    ticker=ticker,
                    price=resp,
                    timestamp=now
                )
                saved += 1
            except Exception as e:
                logger.error(f"Failed [{ticker}]: {e}")
        await session.commit()

    logger.info(f"Saved {saved} price ticks at {now}")
    return saved

@celery_app.task(name="tasks.fetch_prices")
def fetch_prices_task() -> int:
    saved = asyncio.run(fetch_prices())
    return saved