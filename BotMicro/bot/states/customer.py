from aiogram.fsm.state import State, StatesGroup


class ContainerPickupState(StatesGroup):
    docs = State()
    docs_confirmation = State()
    container_type = State()
    terminal = State()
    warehouse = State()
    terminal_delivery = State()
    weight = State()
    special_conditions = State()
    confirmation = State()
    email = State()
