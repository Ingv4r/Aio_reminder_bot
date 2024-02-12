from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.settings import settings, MessageText
from core.utils.fsm import SetRemind
from core.utils.scheduler import SingletonScheduler

router = Router()
TIME_PATTERN = r"^([0-1]?\d|2[0-3]):[0-5]?\d$"


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"{settings.messages.remind_message}")


@router.message(StateFilter(None), Command("add_reminder"))
async def add_new_reminder(message: Message, state: FSMContext):
    await message.answer(
        "Хорошо, давай добвим новое напоминание\n"
        "Введи название напоминания"
    )
    await state.set_state(SetRemind.choosing_remind_name)

@router.message(StateFilter(None), Command("set_remind_time"))
async def set_remind_time(message: Message, state: FSMContext):
    await message.answer(
        "Введи время, когда нужно напомнить\n "
        "Формат: час:минута",
    )
    await state.set_state(SetRemind.choosing_remind_time)


@router.message(SetRemind.choosing_remind_time, F.text.regexp(TIME_PATTERN))
async def time_chosen(message: Message, state: FSMContext):
    hour, minute = list(map(int, message.text.split(":")))
    scheduler = SingletonScheduler().get_scheduler()
    scheduler.modify_job(
        job_id="reminder",
        hour=hour,
        minute=minute
    )
    await message.answer(
        f"Выбрано время - <b>{hour}:{minute}</b>\n"
        f"Тект напоминания: <b>{settings.schedule.remind_message}</b>\n"
        f"Если нужно выставить напоминания, воспользуйся командой: <b>/set_remind_message</b>"
    )
    await state.clear()


@router.message(SetRemind.choosing_remind_time)
async def time_chosen_incorrectly(message: Message):
    await message.answer(
        "Неправильно выбрано время.\n"
        "Нужно ввести в формате час:минута.\n"
        "Например: 10:00"
    )


@router.message(StateFilter(None), Command("set_remind_message"))
async def set_message_to_remind(message: Message, state: FSMContext):
    await message.answer("Выбери сообщение напоминания")
    await state.set_state(SetRemind.choosing_remind_message)


@router.message(SetRemind.choosing_remind_message, F.text)
async def message_chosen(message: Message, state: FSMContext):
    MessageText.remind_message = message.text
    await message.answer(f"Текст напоминаний: <b>{settings.messages.remind_message}</b>")
    await state.clear()


@router.message(SetRemind.choosing_remind_message)
async def message_chosen_incorrectly(message: Message):
    await message.answer("Нужно ввести текст сообщения")
