from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core import settings
from app.core.limiter import get_db_limiter

engine = create_async_engine(
    settings.database_url,
    echo=False,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession)


async def get_session():
    limiter = get_db_limiter()
    async with limiter.semaphore:
        async with SessionLocal() as session:
            yield session
