from aiogram.types import InlineKeyboardButton

from bot.callbacks.start import OpenAboutUsCallback, OpenContactsCallback


def open_about_us_btns():
    return [
        [
            InlineKeyboardButton(
                text='Далее',
                callback_data=OpenAboutUsCallback().pack()
            )
        ]
    ]


def open_contacts_btns():
    return [
        [
            InlineKeyboardButton(
                text='Далее',
                callback_data=OpenContactsCallback().pack()
            )
        ]
    ]
