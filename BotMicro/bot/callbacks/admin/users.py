from aiogram.filters.callback_data import CallbackData


class OpenUsersManageCallback(CallbackData, prefix='open_users_manage'):
    user_key: str
