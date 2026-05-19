from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth_middleware import get_current_user_id
from app.models.asset import Asset
from app.schemas.asset import AssetCreate

router = APIRouter()


@router.get("")
async def list_assets(db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    rows = (await db.scalars(select(Asset).where(Asset.user_id == user_id))).all()
    return rows


@router.post("", status_code=201)
async def create_asset(payload: AssetCreate, db: AsyncSession = Depends(get_db), user_id: UUID = Depends(get_current_user_id)):
    asset = Asset(user_id=user_id, **payload.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset
