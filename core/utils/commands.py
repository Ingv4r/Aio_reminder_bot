from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="cancell", description="Сбросить"),
        BotCommand(
            command="set_time",
            description="Задать время напоминаний в формате hh-hh:mm-mm",
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())