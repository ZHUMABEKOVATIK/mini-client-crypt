from unittest.mock import AsyncMock

from src.services.price import PriceService


async def test_service_create_delegates_to_repository():
    service = PriceService(session=None)
    service.repo = AsyncMock()
    service.repo.create.return_value = "fake_tick"

    result = await service.create(ticker="btc_usd", price=100.0, timestamp=123)

    service.repo.create.assert_awaited_once_with(ticker="btc_usd", price=100.0, timestamp=123)
    assert result == "fake_tick"