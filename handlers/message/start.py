from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import keyboard
import text

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text.hello_username(message.from_user.full_name),
        reply_markup=keyboard.reply.menu())
