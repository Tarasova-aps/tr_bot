from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.customer.callback import StartCallbackCallback
from bot.keyboards.hide_message import hide_message_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.common import WAIT
from bot.messages.customer.callback import (ASK_PHONE, SUCCESS,
                                            build_admin_notification)
from bot.states.customer.callback import CallbackState
from bot.utils.admins import spread_message_to_admins

router = Router()


@router.callback_query(StartCallbackCallback.filter())
async def start_callback_handler(query: CallbackQuery, message: Message, callback_data: StartCallbackCallback, bot: Bot, state: FSMContext):
    callback_init_message = await message.answer(
        text=ASK_PHONE,
        reply_markup=kb_from_btns(hide_message_btns())
    )
    await state.update_data(callback_init_message_id=callback_init_message.message_id)
    await state.set_state(CallbackState.phone)


@router.message(CallbackState.phone, F.text, F.text.as_('phone'))
async def phone_handler(message: Message, phone: str, bot: Bot, state: FSMContext):
    data = await state.get_data()
    callback_init_message_id = data.get('callback_init_message_id')

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=callback_init_message_id,
        text=WAIT,
        reply_markup=kb_from_btns(hide_message_btns())
    )

    await spread_message_to_admins(
        bot=bot,
        text=build_admin_notification(message.chat.full_name, phone),
        reply_markup=kb_from_btns(hide_message_btns())
    )

    await message.delete()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=callback_init_message_id,
        text=SUCCESS,
        reply_markup=kb_from_btns(hide_message_btns())
    )
    await state.clear()
