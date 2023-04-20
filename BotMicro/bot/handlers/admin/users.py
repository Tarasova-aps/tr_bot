from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.admin.users import (DeleteUserCallback, NewAdminCallback,
                                       OpenUserPageCallback,
                                       OpenUsersManageCallback)
from bot.keyboards.admin.menu import open_admin_menu_btns
from bot.keyboards.admin.users import (back_to_users_manage_btns,
                                       delete_user_btns, users_list_btns,
                                       users_manage_btns)
from bot.keyboards.utils import kb_from_btns
from bot.messages.admin.users import (ASK_ADMIN_NAME, SUCCESS_CREATE_ADMIN,
                                      SUCCESS_DELETE_USER, USER_PAGE,
                                      USERS_LIST_TITLE)
from bot.messages.common import WAIT
from bot.states.admin.new_admin import NewAdminState
from bot.utils.init_message import edit_init_message, update_init_message
from models.user import User

router = Router()


@router.callback_query(OpenUsersManageCallback.filter())
async def open_users_manage_handler(query: CallbackQuery, message: Message, callback_data: OpenUsersManageCallback, state: FSMContext):
    users = await User.get_available()

    await update_init_message(
        message, state,
        text=USERS_LIST_TITLE,
        reply_markup=kb_from_btns(
            users_list_btns(callback_data.user_key, users),
            users_manage_btns(callback_data.user_key),
            open_admin_menu_btns(callback_data.user_key)
        )
    )
    await state.clear()


@router.callback_query(NewAdminCallback.filter())
async def new_admin_handler(query: CallbackQuery, message: Message, callback_data: NewAdminCallback, state: FSMContext):
    await update_init_message(
        message, state,
        text=ASK_ADMIN_NAME,
        reply_markup=kb_from_btns(back_to_users_manage_btns(callback_data.user_key))
    )

    await state.update_data(user_key=callback_data.user_key)
    await state.set_state(NewAdminState.name)


@router.message(NewAdminState.name, F.text, F.text.as_('text'))
async def new_admin_name_handler(message: Message, text: str, bot: Bot, state: FSMContext):
    data = await state.get_data()
    user_key: str = data['user_key']

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=WAIT,
        reply_markup=kb_from_btns(back_to_users_manage_btns(user_key))
    )

    user = User(name=text)  # type: ignore
    await user.save()  # type: ignore

    await edit_init_message(
        message, bot, state,
        text=SUCCESS_CREATE_ADMIN(user.name, user.user_key),
        reply_markup=kb_from_btns(back_to_users_manage_btns(user_key))
    )
    await state.clear()


@router.callback_query(OpenUserPageCallback.filter())
async def open_user_page_handler(query: CallbackQuery, message: Message, callback_data: OpenUserPageCallback, state: FSMContext):
    user = await User.get_or_none(callback_data.target_user_key)
    if not user:
        return

    await update_init_message(
        message, state,
        text=USER_PAGE(user.name, user.user_key),
        reply_markup=kb_from_btns(
            delete_user_btns(callback_data.user_key, user.user_key),
            back_to_users_manage_btns(callback_data.user_key)
        )
    )
    await state.clear()


@router.callback_query(DeleteUserCallback.filter())
async def delete_user_handler(query: CallbackQuery, message: Message, callback_data: DeleteUserCallback, state: FSMContext):
    user = await User.get_or_none(callback_data.target_user_key)
    if not user:
        return

    await user.delete()  # type: ignore

    await update_init_message(
        message, state,
        text=SUCCESS_DELETE_USER,
        reply_markup=kb_from_btns(back_to_users_manage_btns(callback_data.user_key))
    )
    await state.clear()
