from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback


def confirm_btns():
    return [
        [
            InlineKeyboardButton(
                text='Подтвердить',
                callback_data=ConfirmCallback().pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data=CancelCallback().pack()
            )
        ]
    ]
