from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.apps_dialogs import ConfirmDocsCallback, SkipContactsCallback
from bot.callbacks.customer.container_pickup import \
    StartContainerPickupCallback


def start_container_pickup_btns():
    return [
        [
            InlineKeyboardButton(
                text='Запрос на автовывоз контейнера',
                callback_data=StartContainerPickupCallback().pack()
            )
        ]
    ]


def confirm_docs_btns():
    return [
        [
            InlineKeyboardButton(
                text='Продолжить',
                callback_data=ConfirmDocsCallback().pack()
            )
        ]
    ]


def skip_contacts_btns():
    return [
        [
            InlineKeyboardButton(
                text='Пропустить',
                callback_data=SkipContactsCallback().pack()
            )
        ]
    ]
