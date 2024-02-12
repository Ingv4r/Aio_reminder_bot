import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import remind, basic, files
from core.settings import settings
from core.utils.scheduler import scheduler


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Принудительно настраиваем фильтр на работу только в чатах один-на-один с ботом
    dp.message.filter(F.chat.type == "private")
    dp.include_routers(basic.router, remind.router, files.router)

    scheduler.start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(message)s"
    )
    asyncio.run(start())
