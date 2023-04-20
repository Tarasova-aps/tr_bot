from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.callback import StartCallbackCallback


def start_callback_btns():
    return [
        [
            InlineKeyboardButton(
                text='Запросить обратный звонок',
                callback_data=StartCallbackCallback().pack()
            )
        ]
    ]
