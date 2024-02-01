from core.settings import settings
from aiogram import Bot


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Так, а ну быстро садись за пет!")
