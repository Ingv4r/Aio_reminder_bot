from datetime import datetime

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F

from core.handlers import basic, apsched
from core.settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import CommandStart

bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")


async def start():
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        apsched.send_message_cron,
        trigger="cron",
        hour=22,
        minute=52,
        start_date=datetime.now(),
        kwargs={"bot": bot}
    )
    scheduler.start()

    dp.startup.register(basic.start_bot)
    dp.shutdown.register(basic.stop_bot)
    dp.message.register(basic.get_photo, F.photo)
    dp.message.register(basic.get_start, CommandStart())
    dp.message.register(basic.get_hello, F.text.lower().in_({"привет", "hello"}))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
