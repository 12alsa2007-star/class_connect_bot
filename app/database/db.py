from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config.settings import settings


# Создание асинхронного engine для PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
)

# Создание асинхронной сессии
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Получить сессию БД"""
    async with async_session() as session:
        yield session


async def init_db():
    """Инициализация БД"""
    async with engine.begin() as conn:
        # Здесь позже будут миграции
        pass