from aiogram.types import InlineKeyboardButton

from bot.callbacks.start import OpenNextGreetingCallback


def open_next_greeting_btns():
    return [
        [
            InlineKeyboardButton(
                text='Далее',
                callback_data=OpenNextGreetingCallback().pack()
            )
        ]
    ]
