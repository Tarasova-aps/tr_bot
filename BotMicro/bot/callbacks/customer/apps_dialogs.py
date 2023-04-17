from aiogram.filters.callback_data import CallbackData


class ConfirmDocsCallback(CallbackData, prefix='confirm_docs'):
    pass


class SkipContactsCallback(CallbackData, prefix='skip_contacts'):
    pass
