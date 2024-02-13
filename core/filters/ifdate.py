from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsMonthDay(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            datetime.strptime(message.text, f"%d.%m.%Y")
            return True
        except ValueError:
            return False
