# tests/test_deribit_client.py
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.deribit_client import DeribitClient


async def test_get_index_price_parses_response():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = AsyncMock(return_value={"result": {"index_price": 65000.42}})

    mock_get_ctx = MagicMock()
    mock_get_ctx.__aenter__ = AsyncMock(return_value=mock_response)
    mock_get_ctx.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.get = MagicMock(return_value=mock_get_ctx)

    mock_session_ctx = MagicMock()
    mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_ctx.__aexit__ = AsyncMock(return_value=None)

    with patch("src.services.deribit_client.aiohttp.ClientSession", return_value=mock_session_ctx):
        client = DeribitClient()
        price = await client.get_index_price("btc_usd")

    assert price == 65000.42