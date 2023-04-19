from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.docs import OpenDocsCallback


def open_info_btns():
    return [
        [
            InlineKeyboardButton(
                text='Документы и контакты',
                callback_data=OpenDocsCallback().pack()
            )
        ]
    ]
