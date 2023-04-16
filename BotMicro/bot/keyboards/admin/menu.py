from aiogram.types import InlineKeyboardButton

from bot.callbacks.admin.applications import OpenApplicationsListCallback
from bot.callbacks.admin.menu import OpenAdminMenuCallback


def open_admin_menu_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Меню',
                callback_data=OpenAdminMenuCallback(user_key=user_key).pack()
            )
        ]
    ]


def back_to_admin_menu_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=OpenAdminMenuCallback(user_key=user_key).pack()
            )
        ]
    ]


def open_applications_list_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Заявки',
                callback_data=OpenApplicationsListCallback(user_key=user_key).pack()
            )
        ]
    ]
