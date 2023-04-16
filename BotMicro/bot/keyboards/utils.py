from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_from_btns(*btns: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    kb_btns: list[list[InlineKeyboardButton]] = []
    for btn in btns:
        kb_btns.extend(btn)

    return InlineKeyboardMarkup(inline_keyboard=kb_btns)
