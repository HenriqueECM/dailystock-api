"""Dependency-style auth helper used by routers to resolve current user from JWT."""
from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise ValueError("wrong token")
        return UUID(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Token inválido") from exc
