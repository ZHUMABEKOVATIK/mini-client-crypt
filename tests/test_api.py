import time
from datetime import datetime, timezone

from src.repositories.price import PriceTickRepository


async def test_get_latest_price_returns_404_when_no_data(client):
    response = await client.get("/api/price/latest", params={"ticker": "btc_usd"})
    assert response.status_code == 404


async def test_get_latest_price_returns_data(client, session):
    repo = PriceTickRepository(session)
    now = int(time.time())
    await repo.create(ticker="btc_usd", price=65000.0, timestamp=now)
    await session.commit()

    response = await client.get("/api/price/latest", params={"ticker": "btc_usd"})
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "btc_usd"
    assert data["price"] == 65000.0


async def test_get_all_prices_requires_ticker_query_param(client):
    response = await client.get("/api/price")
    assert response.status_code == 422


async def test_get_price_history_with_date_filter(client, session):
    repo = PriceTickRepository(session)
    now = int(time.time())
    await repo.create(ticker="btc_usd", price=1.0, timestamp=now - 3600)
    await repo.create(ticker="btc_usd", price=2.0, timestamp=now)
    await session.commit()

    date_from = datetime.fromtimestamp(now - 60, tz=timezone.utc).isoformat()

    response = await client.get(
        "/api/price/history",
        params={"ticker": "btc_usd", "date_from": date_from},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == 2.0