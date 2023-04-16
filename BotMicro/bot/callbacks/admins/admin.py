from typing import Optional
from aiogram.filters.callback_data import CallbackData


class OpenAdminMenuCallback(CallbackData, prefix='open_admin_menu'):
    user_key: Optional[str]
