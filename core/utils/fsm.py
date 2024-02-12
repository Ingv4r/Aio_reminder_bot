from aiogram.fsm.state import StatesGroup, State


class SetRemind(StatesGroup):
    choosing_remind_name = State()
    choosing_remind_time = State()
    choosing_remind_message = State()


