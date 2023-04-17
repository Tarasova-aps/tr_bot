from aiogram.filters.callback_data import CallbackData


class ContainerTypeCallback(CallbackData, prefix='container_type'):
    container_type: str
