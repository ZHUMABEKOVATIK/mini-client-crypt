from sqlalchemy import String, Numeric, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class PriceTick(Base):
    __tablename__ = "price_ticks"
    __table_args__ = (
        Index("ix_price_ticks_ticker_ts", "ticker", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)