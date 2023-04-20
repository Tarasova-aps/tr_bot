from aiogram.fsm.state import State, StatesGroup


class NewAdminState(StatesGroup):
    name = State()
