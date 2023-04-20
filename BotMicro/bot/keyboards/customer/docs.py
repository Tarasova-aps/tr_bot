from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.docs import OpenDocsCallback


def open_docs_btns():
    return [
        [
            InlineKeyboardButton(
                text='Документы',
                callback_data=OpenDocsCallback().pack()
            )
        ]
    ]
