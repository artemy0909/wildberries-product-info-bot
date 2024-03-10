from aiogram.filters.callback_data import CallbackData


class SubscriptionCallback(CallbackData, prefix='sub'):
    article: str


class UnsubscriptionCallback(CallbackData, prefix='unsub'):
    article: str
