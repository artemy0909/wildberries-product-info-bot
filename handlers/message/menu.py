from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboard
import text
from utils import database
from utils.states import MenuCommands

menu_router = Router()


@menu_router.message(F.text == keyboard.MenuButtons.get_product_info)
async def get_product_info_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuCommands.article)
    await message.answer(
        text.SEND_ARTICLE,
        reply_markup=keyboard.reply.back_to_menu()
    )


@menu_router.message(F.text == keyboard.MenuButtons.stop_notifications)
async def stop_notifications_handler(message: Message) -> None:
    from loader import scheduler
    scheduler.remove_all_user_alerts(message.from_user.id)
    await database.unsubscribe_all(message.from_user.id)
    await message.answer(
        text.ALL_NOTIFICATIONS_IS_STOPPED,
        reply_markup=keyboard.reply.menu()
    )


@menu_router.message(F.text == keyboard.MenuButtons.get_database_info)
async def get_database_info_handler(message: Message) -> None:
    last_queries = await database.get_last_user_query_records(message.from_user.id, quantity=5)
    if not last_queries:
        await message.answer(
            "Записей в БД пока нет",
            reply_markup=keyboard.reply.menu()
        )
        return
    await message.answer(
        text.summary_of_queries(last_queries),
        reply_markup=keyboard.reply.menu()
    )


@menu_router.message(MenuCommands.article, F.text == keyboard.MenuButtons.back_to_menu)
async def back_to_menu_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text.USE_BUTTONS,
        reply_markup=keyboard.reply.menu()
    )


@menu_router.message(MenuCommands.article, F.text.regexp(r"^\d+$"))
async def article_handler(message: Message, state: FSMContext) -> None:
    article = message.text
    await database.add_user_query(message.from_user.id, article)
    product = await database.get_product_fresh_record(article)
    if product:
        response_text = text.product_info_to_description(
            product.article,
            product.title,
            product.price,
            product.rating,
            product.quantity
        )
        subscribed = await database.is_subscription_exists(message.from_user.id, product.article)
        if subscribed:
            reply_markup = keyboard.inline.unsubscribe(product.article)
        else:
            reply_markup = keyboard.inline.subscribe(product.article)
        await message.answer(response_text, reply_markup=reply_markup)
        await state.clear()
        await message.answer(
            text.USE_BUTTONS,
            reply_markup=keyboard.reply.menu()
        )
    else:
        await message.answer(text.ARTICLE_NOT_FOUND)


@menu_router.message(MenuCommands.article)
async def article_exception_handler(message: Message) -> None:
    await message.answer(text.WRONG_INPUT)


@menu_router.message()
async def menu_exception_handler(message: Message) -> None:
    await message.answer(
        text.USE_BUTTONS,
        reply_markup=keyboard.reply.menu()
    )
