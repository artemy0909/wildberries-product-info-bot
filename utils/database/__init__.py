from .db import session_factory
from .models import *


def add_user_query(user_id, article):
    with session_factory() as session:
        user_query = UserQuery(telegram_id=user_id, article=article)
        session.add(user_query)
        session.commit()


def subscribe(user_id, article):
    with session_factory() as session:
        subscription = UserSubscription(telegram_id=user_id, article=article)
        session.add(subscription)
        session.commit()


def get_subscription_item(user_id, article) -> UserSubscription:
    with session_factory() as session:
        subscription = session.query(UserSubscription).filter(
            UserSubscription.telegram_id == user_id,
            UserSubscription.article == article
        ).first()
        return subscription


def unsubscribe(user_id, article):
    with session_factory() as session:
        subscription = get_subscription_item(user_id, article)
        session.delete(subscription)
        session.commit()


def unsubscribe_all(user_id):
    with session_factory() as session:
        subscriptions = session.query(UserSubscription).filter(
            UserSubscription.telegram_id == user_id
        ).all()
        for subscription in subscriptions:
            session.delete(subscription)
        session.commit()


def is_subscription_exists(user_id, article):
    subscription = get_subscription_item(user_id, article)
    return subscription is not None


def get_last_user_query_records(user_id, quantity):
    with session_factory() as session:
        user_queries = session.query(UserQuery).filter(
            UserQuery.telegram_id == user_id
        ).order_by(UserQuery.id.desc()).limit(quantity).all()
        return user_queries


def get_all_subscriptions():
    with session_factory() as session:
        subscriptions = session.query(UserSubscription).all()
        return subscriptions
