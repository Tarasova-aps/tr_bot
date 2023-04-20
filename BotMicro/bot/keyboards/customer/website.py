from aiogram.types import InlineKeyboardButton


def website_btns():
    return [
        [
            InlineKeyboardButton(
                text='Наш сайт',
                url='http://transcombinat.ru'
            )
        ]
    ]
