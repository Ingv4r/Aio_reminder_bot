from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import remind
from core.settings import settings


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


def add_reminder(bot, hour, minute, name):
    scheduler.add_job(
        func=remind.send_message_cron,
        id=name,
        trigger="cron",
        hour=hour,
        minute=minute,
        start_date=datetime.now(),
        kwargs={"bot": bot},
    )
