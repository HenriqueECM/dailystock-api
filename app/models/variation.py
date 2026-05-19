import uuid
from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Variation(Base):
    __tablename__ = "variations"
    __table_args__ = (UniqueConstraint("user_id", "ticker", "date", name="uq_variations_user_ticker_date"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    pct_change: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    close_price: Mapped[float | None] = mapped_column(Numeric(12, 4))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
