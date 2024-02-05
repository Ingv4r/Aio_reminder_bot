from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots
    remind_hours_range: list[int]
    remind_minutes_range: list[int]
    remind_message: str


def get_settings():
    return Settings(
        bots=Bots(bot_token=getenv("TOKEN"), admin_id=int(getenv("ADMIN_ID"))),
        remind_message="Напоминание не выставлено",
        remind_hours_range=[0, 23],
        remind_minutes_range=[0, 59],
    )


settings = get_settings()
print(settings)
