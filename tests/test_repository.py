import time


async def test_create_and_get_latest(session):
    from src.repositories.price import PriceTickRepository
    repo = PriceTickRepository(session)
    now = int(time.time())

    await repo.create(ticker="btc_usd", price=65000.5, timestamp=now)
    await repo.create(ticker="btc_usd", price=65100.0, timestamp=now + 60)
    await session.commit()

    latest = await repo.get_latest("btc_usd")
    assert latest is not None
    assert float(latest.price) == 65100.0
    assert latest.timestamp == now + 60


async def test_get_all_by_ticker_filters_by_ticker(session):
    from src.repositories.price import PriceTickRepository
    repo = PriceTickRepository(session)
    now = int(time.time())

    await repo.create(ticker="btc_usd", price=65000.0, timestamp=now)
    await repo.create(ticker="eth_usd", price=3200.0, timestamp=now)
    await session.commit()

    btc_ticks = await repo.get_all_by_ticker("btc_usd")
    assert len(btc_ticks) == 1
    assert btc_ticks[0].ticker == "btc_usd"


async def test_get_by_date_range(session):
    from src.repositories.price import PriceTickRepository
    from datetime import datetime, timezone
    repo = PriceTickRepository(session)
    now = int(time.time())

    await repo.create(ticker="btc_usd", price=1.0, timestamp=now - 3600)
    await repo.create(ticker="btc_usd", price=2.0, timestamp=now)
    await repo.create(ticker="btc_usd", price=3.0, timestamp=now + 3600)
    await session.commit()

    date_from = datetime.fromtimestamp(now - 60, tz=timezone.utc)
    date_to = datetime.fromtimestamp(now + 60, tz=timezone.utc)

    result = await repo.get_by_date_range("btc_usd", date_from, date_to)
    assert len(result) == 1
    assert float(result[0].price) == 2.0


async def test_get_latest_returns_none_when_no_data(session):
    from src.repositories.price import PriceTickRepository
    repo = PriceTickRepository(session)
    result = await repo.get_latest("unknown_ticker")
    assert result is None