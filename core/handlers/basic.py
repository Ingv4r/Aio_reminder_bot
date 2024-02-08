from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text

from core.settings import settings
from core.utils.commands import set_commands


router = Router()


@router.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Бот запущен")


@router.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот становлен")


@router.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    await message.answer("Hello! I'm <b>Aio_Bot</b>")


@router.message(F.text.lower().in_({"привет", "hello", "hi"}))
async def get_hello(message: Message):
    content = Text("И тебе привет, ", Bold(message.from_user.full_name), " !")
    await message.answer(**content.as_kwargs())
