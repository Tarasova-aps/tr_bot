from typing import Optional

from aiogram.types import InlineKeyboardButton

from bot.callbacks.admin import OpenAdminMenuCallback


def open_admin_menu_btns(user_key: Optional[str] = None):
    return [
        [
            InlineKeyboardButton(
                text='Меню',
                callback_data=OpenAdminMenuCallback(user_key=user_key).pack()
            )
        ]
    ]
