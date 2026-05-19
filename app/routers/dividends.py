from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth_middleware import get_current_user_id
from app.models.dividend import Dividend
from app.schemas.dividend import DividendCreate

router = APIRouter()

@router.get("")
async def list_dividends(db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    return (await db.scalars(select(Dividend).where(Dividend.user_id == user_id))).all()

@router.post("", status_code=201)
async def create_dividend(payload: DividendCreate, db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    row = Dividend(user_id=user_id, **payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row
