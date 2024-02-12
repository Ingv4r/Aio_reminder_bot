from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class SchedulerParams:
    remind_hour: int
    remind_minute: int
    remind_message: str = "Текст не задан"


@dataclass
class Settings:
    bots: Bots
    scheduler_params: SchedulerParams


def get_settings():
    return Settings(
        bots=Bots(bot_token=getenv("TOKEN"), admin_id=int(getenv("ADMIN_ID"))),
        scheduler_params=SchedulerParams(remind_hour=0, remind_minute=0)
    )


settings = get_settings()
