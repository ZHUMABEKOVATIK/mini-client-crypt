import aiohttp
from src.core.config import settings

class DeribitClient:
    async def get_index_price(self, index_name: str) -> float:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.DERIBIT_BASE_URL,
                params={"index_name": index_name},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["result"]["index_price"]