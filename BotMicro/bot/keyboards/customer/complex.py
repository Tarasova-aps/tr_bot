from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.complex import StartComplexCallback


def start_complex_btns():
    return [
        [
            InlineKeyboardButton(
                text='Запрос на прием и раскредитацию контейнера и автодоставку',
                callback_data=StartComplexCallback().pack()
            )
        ]
    ]
