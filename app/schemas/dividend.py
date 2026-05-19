from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class DividendCreate(BaseModel):
    asset_id: str
    ticker: str
    payment_date: date
    amount: Decimal
    kind: str = "DIV"
    notes: str | None = None
