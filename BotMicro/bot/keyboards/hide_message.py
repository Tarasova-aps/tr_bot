
from aiogram.types import InlineKeyboardButton

from bot.callbacks.hide_message import HideMessageCallback


def hide_message_btns():
    return [
        [
            InlineKeyboardButton(
                text='Скрыть',
                callback_data=HideMessageCallback().pack()
            )
        ]
    ]
