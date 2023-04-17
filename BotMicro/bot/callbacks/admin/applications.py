from aiogram.filters.callback_data import CallbackData


class OpenApplicationsListCallback(CallbackData, prefix='open_applications_list'):
    user_key: str


class HideApplicationCallback(CallbackData, prefix='hide_application'):
    app_key: str
