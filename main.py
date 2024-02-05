import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from core.handlers import apsched, basic
from core.middlewares.apscheduler_middleware import SchedulerMiddleware
from core.settings import settings
from core.utils.schedule import start_scheduler


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(basic.router, apsched.router)

    start_scheduler(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(message)s"
    )
    asyncio.run(start())
