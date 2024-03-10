from aiogram import Bot

import keyboard
import text
from utils import database
from utils.misc import get_product_info


async def article_alert(bot: Bot, user_id: int, article: str) -> None:
    article_info = get_product_info(article)
    if article_info:
        await bot.send_message(
            chat_id=user_id,
            text=text.SUBSCRIPTION_TITLE + text.product_info_to_description(article_info),
            reply_markup=keyboard.inline.unsubscribe(article))
    else:
        from loader import scheduler
        scheduler.remove_subscribe_alert(user_id, article)
        database.unsubscribe(user_id, article)
        await bot.send_message(
            chat_id=user_id,
            text=text.SUBSCRIPTION_TITLE + text.cannot_find_article(article),
            reply_markup=keyboard.inline.unsubscribe(article))
