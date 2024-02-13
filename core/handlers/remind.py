from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.settings import settings
from core.utils.fsm import SetRemind
from core.utils.scheduler import scheduler
from core.filters.ifdate import IsMonthDay

router = Router()
TIME_PATTERN = r"^([0-1]?\d|2[0-3]):[0-5]?\d$"


async def send_message_cron(bot: Bot, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        settings.bots.admin_id,
        user_data['chosen_message']
    )


@router.message(StateFilter(None), Command("addreminder"))
async def cmd_reminder(message: Message, state: FSMContext):
    await message.answer(
        "Хорошо, давай добвим новое напоминание\n"
        "Введи название напоминания"
    )
    await state.set_state(SetRemind.choosing_remind_name)


@router.message(SetRemind.choosing_remind_name, F.text)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text.lower())
    await message.answer(
        f"Выбрано имя: <b>{message.text.lower()}</b>\n"
        "Теперь введи дату, когда нужно напомнить\n "
        "<b>Формат: день.месяц.год</b>",
    )
    await state.set_state(SetRemind.choosing_remind_date)


@router.message(SetRemind.choosing_remind_date, IsMonthDay())
async def date_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    await message.answer(
        f"Выбрана дата <b>{message.text.lower()}</b>\n"
        "Теперь выбери время\n"
        "Формат: <b>час:минута</b>"
    )
    await state.set_state(SetRemind.choosing_remind_time)


@router.message(SetRemind.choosing_remind_date)
async def date_chosen_incorrectly(message: Message):
    await message.answer(
        "Неправильно выбрана дата\n"
        "Проверь, есть ли такая дата\n"
        "<b>Формат: день.месяц.год</b>"
    )


@router.message(SetRemind.choosing_remind_time, F.text.regexp(TIME_PATTERN))
async def time_chosen(message: Message, state: FSMContext):
    date = await state.get_data()
    await state.update_data(chosen_date=date["chosen_date"] + " " + message.text)
    await message.answer(
        f"Выбрано время - <b>message.text</b>\n"
        "Теперь напиши текст напоминания"
    )
    await state.set_state(SetRemind.choosing_remind_message)


@router.message(SetRemind.choosing_remind_time)
async def time_chosen_incorrectly(message: Message):
    await message.answer(
        "Неправильно выбрано время.\n"
        "Нужно ввести в формате час:минута.\n"
        "Например: 10:00"
    )


@router.message(SetRemind.choosing_remind_message, F.text)
async def message_chosen(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(chosen_message=message.text)
    user_data = await state.get_data()
    run_date = datetime.strptime(user_data["chosen_date"], '%d.%m.%Y %H:%M')
    scheduler.add_job(
        func=send_message_cron,
        id=user_data["chosen_name"],
        trigger="date",
        run_date=run_date,
        kwargs={"bot": bot, "state": state},
    )
    scheduler.start()
    await message.answer(
        f"Отлично, напоминание выставлено на\n"
        f"{user_data}"
    )
    await state.set_state(state=None)
    await message.answer(f"{user_data}")


@router.message(SetRemind.choosing_remind_message)
async def message_chosen_incorrectly(message: Message):
    await message.answer("Нужно ввести текст сообщения")
