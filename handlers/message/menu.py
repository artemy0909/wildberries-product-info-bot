from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboard
import text
from utils import database
from utils.database import add_user_query
from utils.misc import get_product_info
from utils.states import MenuCommands

menu_router = Router()


@menu_router.message(F.text == keyboard.MenuButtons.get_product_info)
async def get_product_info_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuCommands.article)
    await message.answer(
        text.SEND_ARTICLE,
        reply_markup=keyboard.reply.back_to_menu())


@menu_router.message(F.text == keyboard.MenuButtons.stop_notifications)
async def stop_notifications_handler(message: Message) -> None:
    from loader import scheduler
    scheduler.remove_all_user_alerts(message.from_user.id)
    database.unsubscribe_all(message.from_user.id)
    await message.answer(
        text.ALL_NOTIFICATIONS_IS_STOPPED,
        reply_markup=keyboard.reply.menu())


@menu_router.message(F.text == keyboard.MenuButtons.get_database_info)
async def get_database_info_handler(message: Message) -> None:
    last_queries = database.get_last_user_query_records(message.from_user.id, quantity=5)
    await message.answer(
        text.summary_of_queries(last_queries),
        reply_markup=keyboard.reply.menu())


@menu_router.message(MenuCommands.article, F.text == keyboard.MenuButtons.back_to_menu)
async def back_to_menu_handler(message: Message, state: FSMContext) -> None:
    if message.text == keyboard.MenuButtons.back_to_menu:
        await state.clear()
        await message.answer(
            text.USE_BUTTONS,
            reply_markup=keyboard.reply.menu())


@menu_router.message(MenuCommands.article, F.text.regexp(r"^\d+$"))
async def article_handler(message: Message, state: FSMContext) -> None:
    article_info = get_product_info(message.text)
    if article_info:
        add_user_query(user_id=message.from_user.id, article=message.text)
        await state.clear()
        if database.is_subscription_exists(message.from_user.id, article_info.article):
            reply_markup = keyboard.inline.unsubscribe(article_info.article)
        else:
            reply_markup = keyboard.inline.subscribe(article_info.article)
        await message.answer(
            text.product_info_to_description(article_info),
            reply_markup=reply_markup)
        await message.answer(
            text.USE_BUTTONS,
            reply_markup=keyboard.reply.menu())
    else:
        await message.answer(
            text.ARTICLE_NOT_FOUND)


@menu_router.message(MenuCommands.article)
async def article_exception_handler(message: Message) -> None:
    await message.answer(
        text.WRONG_INPUT)


@menu_router.message()
async def menu_exception_handler(message: Message) -> None:
    await message.answer(
        text.USE_BUTTONS,
        reply_markup=keyboard.reply.menu())
