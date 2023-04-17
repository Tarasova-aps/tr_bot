from aiogram.fsm.state import State, StatesGroup


class ContainerPickupState(StatesGroup):
    container_type = State()
    terminal = State()
    warehouse = State()
    terminal_delivery = State()
    weight = State()
    special_conditions = State()
    docs = State()
    contacts = State()
    confirmation = State()


class ComplexState(StatesGroup):
    container_type = State()
    terminal = State()
    warehouse = State()
    terminal_delivery = State()
    weight = State()
    special_conditions = State()
    docs = State()
    contacts = State()
    confirmation = State()
