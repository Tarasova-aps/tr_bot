from aiogram.types import InlineKeyboardButton

from bot.callbacks.admin.users import (DeleteUserCallback, NewAdminCallback,
                                       OpenUserPageCallback, OpenUsersManageCallback)
from models.user import User


def open_users_manage_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Пользователи',
                callback_data=OpenUsersManageCallback(user_key=user_key).pack()
            )
        ]
    ]


def back_to_users_manage_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data=OpenUsersManageCallback(user_key=user_key).pack()
            )
        ]
    ]


def users_list_btns(user_key: str, users: list[User]):
    return [
        [
            InlineKeyboardButton(
                text=user.name,
                callback_data=OpenUserPageCallback(user_key=user_key, target_user_key=user.user_key).pack()
            )
        ]
        for user in users
    ]


def users_manage_btns(user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Добавить администратора',
                callback_data=NewAdminCallback(user_key=user_key).pack()
            )
        ]
    ]


def delete_user_btns(user_key: str, target_user_key: str):
    return [
        [
            InlineKeyboardButton(
                text='❌ Удалить ❌',
                callback_data=DeleteUserCallback(user_key=user_key, target_user_key=target_user_key).pack()
            )
        ]
    ]
