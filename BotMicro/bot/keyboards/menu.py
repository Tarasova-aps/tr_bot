from aiogram.types import InlineKeyboardButton

from bot.callbacks.menu import OpenMenuCallback


def open_menu_btns():
    return [
        [
            InlineKeyboardButton(
                text='Меню',
                callback_data=OpenMenuCallback().pack()
            )
        ]
    ]
