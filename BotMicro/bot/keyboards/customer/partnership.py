from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.partnership import StartPartnershipCallback


def start_partnership_btns():
    return [
        [
            InlineKeyboardButton(
                text='Предложить партнерские услуги',
                callback_data=StartPartnershipCallback().pack()
            )
        ]
    ]
