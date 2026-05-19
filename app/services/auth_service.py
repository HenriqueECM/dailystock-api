from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, payload: UserCreate):
        exists = await self.db.scalar(select(User).where(User.email == payload.email))
        if exists:
            raise HTTPException(status_code=409, detail="E-mail já cadastrado")
        user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password))
        self.db.add(user)
        await self.db.commit()
        return {"id": str(user.id), "email": user.email}

    async def login(self, email: str, password: str):
        user = await self.db.scalar(select(User).where(User.email == email))
        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        claims = {"sub": str(user.id), "email": user.email}
        return {"access_token": create_access_token(claims), "refresh_token": create_refresh_token(claims), "token_type": "bearer"}

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh token inválido")
        claims = {"sub": payload["sub"], "email": payload["email"]}
        return {"access_token": create_access_token(claims), "refresh_token": create_refresh_token(claims), "token_type": "bearer"}

    @staticmethod
    async def google_auth_url():
        return {"message": "Configure Authlib para ativar fluxo OAuth Google"}

    async def google_callback(self, code: str):
        return {"message": "callback placeholder", "code": code}
