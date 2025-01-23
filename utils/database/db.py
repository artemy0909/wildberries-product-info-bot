from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .models import Base
from .config import get_db_url
from ..config import Config

engine = create_async_engine(
    get_db_url(),
    echo=False,
    future=True,
    pool_size=10,  # Размер пула соединений
    max_overflow=20,  # Максимальное количество дополнительных соединений
    pool_timeout=30,  # Таймаут ожидания соединения
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=1800  # Переподключение каждые 30 минут
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    # Проверяем и создаем базу данных при необходимости

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
