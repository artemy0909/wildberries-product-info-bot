from aiogram.utils.keyboard import InlineKeyboardBuilder

from ._callbacks import SubscriptionCallback, UnsubscriptionCallback
from ..buttons import SubInlineButtons


def subscribe(article: str):
    return InlineKeyboardBuilder().button(
        text=SubInlineButtons.subscribe,
        callback_data=SubscriptionCallback(article=article).pack(),
    ).as_markup()


def unsubscribe(article: str):
    return InlineKeyboardBuilder().button(
        text=SubInlineButtons.unsubscribe,
        callback_data=UnsubscriptionCallback(article=article).pack(),
    ).as_markup()
