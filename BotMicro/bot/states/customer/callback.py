from aiogram.fsm.state import State, StatesGroup


class CallbackState(StatesGroup):
    phone = State()
