from fastapi import APIRouter, Query, HTTPException
from datetime import datetime

from src.dependencies import AsyncSessionDep
from src.services.price import PriceService
from src.schemas.price import PriceTickResponse

router = APIRouter(prefix="/price", tags=["Prices"])

@router.get("", response_model=list[PriceTickResponse])
async def get_all_prices(session: AsyncSessionDep, ticker: str = Query(...)):
    service = PriceService(session)
    return await service.get_all_by_ticker(ticker)


@router.get("/latest", response_model=PriceTickResponse)
async def get_latest_price(session: AsyncSessionDep, ticker: str = Query(...)):
    service = PriceService(session)
    tick = await service.get_latest(ticker)

    if tick is None:
        raise HTTPException(status_code=404, detail="No data for this ticker")

    return tick

@router.get("/history", response_model=list[PriceTickResponse])
async def get_price_history(
    session: AsyncSessionDep,
    ticker: str = Query(...),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
):
    service = PriceService(session)
    return await service.get_by_date_range(ticker, date_from, date_to)