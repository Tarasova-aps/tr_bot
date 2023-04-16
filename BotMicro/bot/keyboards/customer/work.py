from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.work import StartWorkCallback


def start_work_btns():
    return [
        [
            InlineKeyboardButton(
                text='Отправить резюме',
                callback_data=StartWorkCallback().pack()
            )
        ]
    ]
