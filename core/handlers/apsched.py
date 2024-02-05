from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from core.settings import settings

router = Router()


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"{settings.remind_message}")


@router.message(F.text, Command("set_time"))
async def set_time_to_remind(message: Message):
    await message.answer(
        "Введи диапазон времени, "
        "когда ты хочешь получать напоминания в формате: \n<b>h:m - h:m</b>"
    )
