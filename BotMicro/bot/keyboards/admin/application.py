from aiogram.types import InlineKeyboardButton

from bot.callbacks.admin.applications import HideApplicationCallback


def hide_application_btns(app_key: str):
    return [
        [
            InlineKeyboardButton(
                text='Скрыть',
                callback_data=HideApplicationCallback(app_key=app_key).pack(),
            )
        ]
    ]
