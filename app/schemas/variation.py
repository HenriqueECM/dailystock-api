from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class VariationCreate(BaseModel):
    asset_id: str
    ticker: str
    date: date
    pct_change: Decimal
    close_price: Decimal | None = None
