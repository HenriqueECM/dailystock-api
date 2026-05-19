from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.middleware.rate_limit import RateLimitMiddleware
from app.routers import auth, assets, variations, dividends, dashboard
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create schema on startup in dev environments."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title='EquitySaaS API', version='1.0.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(RateLimitMiddleware)

app.include_router(auth.router)
app.include_router(assets.router, prefix='/assets', tags=['assets'])
app.include_router(variations.router, prefix='/variations', tags=['variations'])
app.include_router(dividends.router, prefix='/dividends', tags=['dividends'])
app.include_router(dashboard.router, prefix='/dashboard', tags=['dashboard'])


@app.get('/health')
async def health():
    return {'status': 'ok', 'service': settings.APP_NAME}
