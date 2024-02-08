from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.settings import settings
from core.utils.fsm import SetRemindTime

router = Router()


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"{settings.remind_message}")


@router.message(StateFilter(None), Command("set_time"))
async def set_time_to_remind(message: Message, state: FSMContext):
    await message.answer(
        "Введи часы, в которые будут отправляться напоминания \n "
        "Формат: час-час",
    )
    await state.set_state(SetRemindTime.hours)


@router.message(
    SetRemindTime.hours,
    F.text.regexp(r"(([0-1]?\d)|(2[0-3]))-(([0-1]?\d)|(2[0-3]))")
)
async def hours_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_hours=message.text)
    await message.answer("Тепепь выбери минуты. Формат: минута-минута")
    await state.set_state(SetRemindTime.minutes)


@router.message(SetRemindTime.hours)
async def hours_chosen_incorrectly(message: Message):
    await message.answer(
        "Неправильно выбраны часы. \n\nВведи часы от 0 до 23. "
        "Формат: час-час"
    )


@router.message(
    SetRemindTime.minutes,
    F.text.regexp(r"[0-5]?\d-[0-5]?\d")
)
async def minutes_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    hour1, hour2 = user_data["chosen_hours"].split("-")
    minute1, minute2 = message.text.split("-")
    await message.answer(
        f"Напоминания будут приходить в период с {hour1}:{minute1} "
        f"по {hour2}:{minute2}"
    )
    await state.clear()


@router.message(SetRemindTime.minutes)
async def minutes_chosen_incorrectly(message: Message):
    await message.answer(
        "Неправильно выбраны минуты. \n\nВведи минуты от 0 до 59. "
        "Формат: минута-минута"
    )
