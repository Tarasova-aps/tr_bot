from aiogram.types import InlineKeyboardButton


def start_container_pickup_btns():
    return [
        [
            InlineKeyboardButton(
                text='Запрос на автовывоз контейнера',
                url='https://forms.yandex.ru/u/643fe04be010db11eb5a51a9/'
            )
        ]
    ]
