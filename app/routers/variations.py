from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth_middleware import get_current_user_id
from app.models.variation import Variation
from app.schemas.variation import VariationCreate

router = APIRouter()

@router.get("")
async def list_variations(db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id), ticker: str | None = None):
    q = select(Variation).where(Variation.user_id == user_id)
    if ticker:
        q = q.where(Variation.ticker == ticker)
    return (await db.scalars(q)).all()

@router.post("", status_code=201)
async def create_variation(payload: VariationCreate, db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    row = Variation(user_id=user_id, **payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row
