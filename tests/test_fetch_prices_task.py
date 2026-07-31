from unittest.mock import AsyncMock, patch

import src.tasks.fetch_prices as task_module
from src.repositories.price import PriceTickRepository


async def test_fetch_prices_saves_both_tickers(session, monkeypatch):
    class FakeSessionCtx:
        async def __aenter__(self):
            return session
        async def __aexit__(self, *args):
            pass

    monkeypatch.setattr(task_module, "async_session", lambda: FakeSessionCtx())

    with patch.object(
        task_module.DeribitClient, "get_index_price",
        new=AsyncMock(side_effect=[65000.0, 3200.0]),
    ):
        saved = await task_module.fetch_prices()

    assert saved == 2

    repo = PriceTickRepository(session)
    btc = await repo.get_latest("btc_usd")
    eth = await repo.get_latest("eth_usd")
    assert float(btc.price) == 65000.0
    assert float(eth.price) == 3200.0