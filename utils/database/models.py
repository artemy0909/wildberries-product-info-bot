from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, BigInteger, Float, DateTime, func


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    price: Mapped[int] = mapped_column(Integer, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )


class UserQuery(Base):
    __tablename__ = "user_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    article: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __str__(self):
        return f"Пользователь: <i>{self.telegram_id}</i>\n" \
               f"Артикул: <i>{self.article}</i>\n" \
               f"Время: <i>{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</i>"


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    article: Mapped[str] = mapped_column(String)


class UpdateSchedules(Base):
    __tablename__ = "update_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article: Mapped[str] = mapped_column(String)
