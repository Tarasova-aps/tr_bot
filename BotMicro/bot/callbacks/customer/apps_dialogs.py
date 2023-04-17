from aiogram.filters.callback_data import CallbackData


class ConfirmDocsCallback(CallbackData, prefix='confirm_docs'):
    pass


class ContainerTypeCallback(CallbackData, prefix='container_type'):
    container_type: str
