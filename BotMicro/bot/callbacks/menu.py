from typing import Optional
from aiogram.filters.callback_data import CallbackData


class OpenMenuCallback(CallbackData, prefix='open_menu'):
    user_key: Optional[str]
