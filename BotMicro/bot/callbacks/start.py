from aiogram.filters.callback_data import CallbackData


class OpenAboutUsCallback(CallbackData, prefix='open_about_us'):
    pass


class OpenContactsCallback(CallbackData, prefix='open_contacts'):
    pass
