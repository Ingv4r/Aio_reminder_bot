from datetime import datetime
from random import randint

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import apsched
from core.settings import settings


def start_scheduler(bot: Bot) -> None:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        apsched.send_message_cron,
        trigger="cron",
        hour=randint(*settings.remind_hours_range),
        minute=randint(*settings.remind_minutes_range),
        start_date=datetime.now(),
        kwargs={"bot": bot},
    )
    scheduler.start()
