from aiogram import Router
from aiogram.types import CallbackQuery

import keyboard
import text
from keyboard.inline import SubscriptionCallback, UnsubscriptionCallback
from utils import database
from utils.config import Config

subscribe_router = Router()


@subscribe_router.callback_query(SubscriptionCallback.filter())
async def sub_inline_callback(query: CallbackQuery, callback_data: SubscriptionCallback):
    article = callback_data.article
    if await database.is_subscription_exists(query.from_user.id, article):
        await query.answer(text.SUBSCRIPTION_ALREADY_EXISTS, show_alert=True)
    else:
        from loader import scheduler
        scheduler.add_subscribe_alert(query.from_user.id, article, Config.SUBSCRIBE_PUSH_INTERVAL)
        await database.subscribe(query.from_user.id, article)
    await query.message.edit_reply_markup(reply_markup=keyboard.inline.unsubscribe(article))


@subscribe_router.callback_query(UnsubscriptionCallback.filter())
async def unsub_inline_callback(query: CallbackQuery, callback_data: UnsubscriptionCallback):
    article = callback_data.article
    if await database.is_subscription_exists(query.from_user.id, article):
        from loader import scheduler
        scheduler.remove_subscribe_alert(query.from_user.id, article)
        await database.unsubscribe(query.from_user.id, article)
    else:
        await query.answer(text.UNSUBSCRIPTION_NOT_EXISTS, show_alert=True)
    await query.message.edit_reply_markup(reply_markup=keyboard.inline.subscribe(article))
