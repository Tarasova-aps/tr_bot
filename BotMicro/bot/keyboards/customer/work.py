from aiogram.types import InlineKeyboardButton


def start_work_btns():
    return [
        [
            InlineKeyboardButton(
                text='Отправить резюме',
                url='https://forms.yandex.ru/u/643fe981068ff01298ac9c99/'
            )
        ]
    ]
