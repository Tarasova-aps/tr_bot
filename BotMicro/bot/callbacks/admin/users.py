from aiogram.filters.callback_data import CallbackData


class OpenUsersManageCallback(CallbackData, prefix='open_users_manage'):
    user_key: str


class NewAdminCallback(CallbackData, prefix='new_admin'):
    user_key: str


class OpenUserPageCallback(CallbackData, prefix='open_user_page'):
    user_key: str
    target_user_key: str


class DeleteUserCallback(CallbackData, prefix='delete_user'):
    user_key: str
    target_user_key: str
