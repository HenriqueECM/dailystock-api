from decimal import Decimal
from pydantic import BaseModel


class AssetCreate(BaseModel):
    ticker: str
    company_name: str | None = None
    avg_price: Decimal
    shares: Decimal


class AssetOut(AssetCreate):
    id: str
