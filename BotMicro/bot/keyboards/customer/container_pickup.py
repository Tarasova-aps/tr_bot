from aiogram.types import InlineKeyboardButton

from bot.callbacks.customer.container_pickup import \
    StartContainerPickupCallback
from bot.callbacks.customer.container_type import ContainerTypeCallback


def start_container_pickup_btns():
    return [
        [
            InlineKeyboardButton(
                text='Запрос на автовывоз контейнера',
                callback_data=StartContainerPickupCallback().pack()
            )
        ]
    ]


def container_type_btns():
    return [
        [
            InlineKeyboardButton(
                text='40НС',
                callback_data=ContainerTypeCallback(container_type='40НС').pack()
            ),
            InlineKeyboardButton(
                text='45НС',
                callback_data=ContainerTypeCallback(container_type='45НС').pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='40Реф',
                callback_data=ContainerTypeCallback(container_type='40Реф').pack()
            ),
            InlineKeyboardButton(
                text='20Реф',
                callback_data=ContainerTypeCallback(container_type='20Реф').pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='20ф',
                callback_data=ContainerTypeCallback(container_type='20ф').pack()
            ),
            InlineKeyboardButton(
                text='20НС',
                callback_data=ContainerTypeCallback(container_type='20НС').pack()
            )
        ],
        [
            InlineKeyboardButton(
                text='20реф',
                callback_data=ContainerTypeCallback(container_type='20реф').pack()
            ),
            InlineKeyboardButton(
                text='40 Опентоп',
                callback_data=ContainerTypeCallback(container_type='40 Опентоп').pack()
            )
        ]
    ]
