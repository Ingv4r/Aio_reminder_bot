from aiogram.fsm.state import StatesGroup, State


class SetRemindTime(StatesGroup):
    hours = State()
    minutes = State()
