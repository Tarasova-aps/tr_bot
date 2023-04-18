from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.partnership import StartPartnershipCallback


def start_partnership_btns():
    return [
        [
            InlineKeyboardButton(
                text='Предложение от Транспортных компаний и Предпринимателей о совместной работе',
                callback_data=StartPartnershipCallback().pack()
            )
        ]
    ]
