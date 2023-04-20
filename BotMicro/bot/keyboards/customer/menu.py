from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.menu import OpenMenuCallback


def open_menu_btns():
    return [
        [
            InlineKeyboardButton(
                text='Меню',
                callback_data=OpenMenuCallback().pack()
            )
        ]
    ]
