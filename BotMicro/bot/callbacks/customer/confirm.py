from aiogram.filters.callback_data import CallbackData


class ConfirmCallback(CallbackData, prefix='confirm'):
    pass


class CancelCallback(CallbackData, prefix='cancel'):
    pass
