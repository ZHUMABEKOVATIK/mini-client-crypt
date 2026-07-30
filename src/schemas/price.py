from pydantic import BaseModel, ConfigDict

class PriceTickResponse(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int

    model_config = ConfigDict(from_attributes=True)