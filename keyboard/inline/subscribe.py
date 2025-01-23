from aiogram.utils.keyboard import InlineKeyboardBuilder

from ._callbacks import SubscriptionCallback, UnsubscriptionCallback
from ..buttons import SubInlineButtons


def subscribe(article: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=SubInlineButtons.subscribe,
        callback_data=SubscriptionCallback(article=article)
    )
    return builder.as_markup()


def unsubscribe(article: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=SubInlineButtons.unsubscribe,
        callback_data=UnsubscriptionCallback(article=article)
    )
    return builder.as_markup()
