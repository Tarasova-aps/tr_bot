from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.info import OpenInfoCallback


def open_info_btns():
    return [
        [
            InlineKeyboardButton(
                text='Документы и контакты',
                callback_data=OpenInfoCallback().pack()
            )
        ]
    ]
