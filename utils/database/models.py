from datetime import datetime

from aiogram.utils.markdown import hcode
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class UserQuery(Base):
    __tablename__ = 'user_queries'

    id: Mapped[int] = Column(Integer, primary_key=True)
    telegram_id: Mapped[int] = Column(BigInteger, index=True)
    article: Mapped[str] = Column(String)
    timestamp: Mapped[datetime] = Column(DateTime, default=func.now())

    def __repr__(self):
        return (f"<UserQuery(id={self.id}, telegram_id={self.telegram_id},"
                f"article='{self.article}, timestamp={self.timestamp}')>")

    def __str__(self):
        return (f"UserQuery #{hcode(self.id)}\ntelegram_id: {hcode(self.telegram_id)}\narticle: {hcode(self.article)}\n"
                f"timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M')}\n")


class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'

    id: Mapped[int] = Column(Integer, primary_key=True)
    telegram_id: Mapped[int] = Column(BigInteger, index=True)
    article: Mapped[str] = Column(String)

    def __repr__(self):
        return (f"<UserSubscription(id={self.id}, telegram_id={self.telegram_id},"
                f"article='{self.article}')>")
