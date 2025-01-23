from aiogram import Bot

import keyboard
import text
from utils.database import unsubscribe, is_subscription_exists, add_product_data, get_product_fresh_record
from utils.wildberries import fetch_product_info


async def article_alert(bot: Bot, user_id: int, article: str) -> None:
    product_info = await fetch_product_info(article)
    if product_info:
        await add_product_data(product_info)
        if not await is_subscription_exists(user_id, article):
            return

        fresh = await get_product_fresh_record(article)
        if fresh:
            msg_text = text.SUBSCRIPTION_TITLE + text.product_info_to_description(
                fresh.article,
                fresh.title,
                fresh.price,
                fresh.rating,
                fresh.quantity
            )
            await bot.send_message(
                chat_id=user_id,
                text=msg_text,
                reply_markup=keyboard.inline.unsubscribe(article)
            )
        else:
            await unsubscribe(user_id, article)
            from loader import scheduler
            scheduler.remove_subscribe_alert(user_id, article)
            await bot.send_message(
                chat_id=user_id,
                text=text.SUBSCRIPTION_TITLE + text.cannot_find_article(article),
                reply_markup=keyboard.inline.unsubscribe(article)
            )
