import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from app.config.settings import settings


# -------- DATABASE URL FIX --------
DATABASE_URL = settings.DATABASE_URL

# Render даёт обычный URL → превращаем в asyncpg формат
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://"
    )


# -------- ENGINE --------
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,   # безопаснее на Render
)


# -------- SESSION --------
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -------- DEPENDENCY --------
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# -------- INIT DB --------
async def init_db():
    async with engine.begin() as conn:
        # пока без миграций
        pass