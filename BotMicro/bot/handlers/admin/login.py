from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.admin.menu import open_admin_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.admin.login import (ASK_ACCESS_KEY, GREET_ADMIN,
                                INCORRECT_ACCESS_KEY)
from bot.states.admin import LoginState
from bot.utils.init_message import edit_init_message, resend_init_message
from models.user import User

router = Router()


@router.message(Command('admin'))
async def admin_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    await resend_init_message(
        message, bot, state,
        text=ASK_ACCESS_KEY
    )
    await state.set_state(LoginState.access_key)


@router.message(LoginState.access_key, F.text, F.text.as_('text'))
async def access_key_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    await message.delete()
    user = await User.get_or_none(text)
    if not user:
        await edit_init_message(
            message, bot, state,
            text=INCORRECT_ACCESS_KEY
        )
        return

    user.chat_id = message.chat.id
    await user.save()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text=GREET_ADMIN(user.name),
        reply_markup=kb_from_btns(open_admin_menu_btns(user.user_key))
    )
    await state.clear()
