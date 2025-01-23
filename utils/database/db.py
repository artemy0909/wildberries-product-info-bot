from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .config import get_db_url
from .models import Base

engine = create_async_engine(
    get_db_url(),
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=1800
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
