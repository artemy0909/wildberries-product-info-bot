from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.wildberries import ProductInfo

from datetime import datetime

from sqlalchemy import select

from .db import async_session_factory
from .models import Product, UserQuery, UserSubscription, UpdateSchedules


async def add_product_data(product_info: "ProductInfo"):
    async with async_session_factory() as session:
        result = await session.execute(
            select(Product).where(Product.article == product_info.article)
        )
        existing = result.scalars().first()
        if existing:
            existing.title = product_info.title
            existing.rating = product_info.rating
            existing.price = product_info.price
            existing.quantity = product_info.quantity
            existing.updated_at = datetime.utcnow()
        else:
            new_item = Product(
                article=product_info.article,
                title=product_info.title,
                rating=product_info.rating,
                price=product_info.price,
                quantity=product_info.quantity
            )
            session.add(new_item)
        await session.commit()


async def get_product_fresh_record(article: str) -> Product | None:
    async with async_session_factory() as session:
        result = await session.execute(
            select(Product).where(Product.article == article)
        )
        return result.scalars().first()


async def add_user_query(user_id: int, article: str):
    async with async_session_factory() as session:
        q = UserQuery(telegram_id=user_id, article=article)
        session.add(q)
        await session.commit()


async def get_last_user_query_records(user_id: int, quantity: int):
    async with async_session_factory() as session:
        result = await session.execute(
            select(UserQuery)
            .where(UserQuery.telegram_id == user_id)
            .order_by(UserQuery.id.desc())
            .limit(quantity)
        )
        return result.scalars().all()


async def subscribe(user_id: int, article: str):
    async with async_session_factory() as session:
        sub = UserSubscription(telegram_id=user_id, article=article)
        session.add(sub)
        await session.commit()


async def unsubscribe(user_id: int, article: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(UserSubscription).where(
                UserSubscription.telegram_id == user_id,
                UserSubscription.article == article
            )
        )
        sub = result.scalars().first()
        if sub:
            await session.delete(sub)
            await session.commit()


async def schedule_update(article: str):
    async with async_session_factory() as session:
        schedule = UpdateSchedules(article=article)
        session.add(schedule)
        await session.commit()


async def unsubscribe_all(user_id: int):
    async with async_session_factory() as session:
        result = await session.execute(
            select(UserSubscription).where(UserSubscription.telegram_id == user_id)
        )
        subs = result.scalars().all()
        for sub in subs:
            await session.delete(sub)
            await session.commit()


async def is_subscription_exists(user_id: int, article: str) -> bool:
    async with async_session_factory() as session:
        result = await session.execute(
            select(UserSubscription).where(
                UserSubscription.telegram_id == user_id,
                UserSubscription.article == article
            )
        )
        sub = result.scalars().first()
        return sub is not None


async def get_all_subscriptions():
    async with async_session_factory() as session:
        result = await session.execute(select(UserSubscription))
        return result.scalars().all()


async def get_all_update_schedules():
    async with async_session_factory() as session:
        result = await session.execute(select(UpdateSchedules))
        return result.scalars().all()
