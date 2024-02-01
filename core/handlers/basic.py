from aiogram.types import Message

from core.settings import settings
from aiogram import Bot

HIGHEST_RESOL_INDEX = -1


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот становлен")


async def get_photo(message: Message, bot: Bot):
    await message.answer("Saving the image")
    file = await bot.get_file(message.photo[HIGHEST_RESOL_INDEX].file_id)
    await bot.download_file(file.file_path, "saving images/image.jpg")


async def get_start(message: Message, bot: Bot):
    await message.answer("Hello! I'm Aio_Bot")


async def get_hello(message: Message):
    await message.answer(f"И тебе привет, <b>{message.from_user.full_name}</b>!")
