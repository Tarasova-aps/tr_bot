from aiogram.types import InlineKeyboardButton

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
