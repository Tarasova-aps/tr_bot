from os import getenv

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.admin.menu import OpenAdminMenuCallback
from bot.keyboards.admin.menu import open_applications_list_btns
from bot.keyboards.admin.users import open_users_manage_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.admin.menu import TITLE
from bot.utils.init_message import update_init_message

router = Router()


@router.callback_query(OpenAdminMenuCallback.filter())
async def open_admin_menu(query: CallbackQuery, message: Message, callback_data: OpenAdminMenuCallback, state: FSMContext):
    await state.clear()

    if callback_data.user_key == getenv('ROOT_ADMIN_KEY'):
        btns = [
            open_users_manage_btns(callback_data.user_key),
            open_applications_list_btns(callback_data.user_key)
        ]
    else:
        btns = [
            open_applications_list_btns(callback_data.user_key)
        ]

    await update_init_message(
        message, state,
        text=TITLE,
        reply_markup=kb_from_btns(*btns)
    )
