from typing import BinaryIO, Optional

from aiogram import Bot, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback
from bot.callbacks.customer.work import StartWorkCallback
from bot.keyboards.customer.confirm import confirm_btns
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.apps_dialogs import (ASK_CONFIRMATION, ASK_CV,
                                                REJECT, SUCCESS_APPLICATION)
from bot.states.customer import WorkState
from bot.utils.application import spread_application_to_admins
from models.application import Application
from models.user import User
from utils.drive import upload_file

router = Router()


@router.callback_query(StartWorkCallback.filter())
async def start_work_handler(query: CallbackQuery, message: Message, callback_data: StartWorkCallback, state: FSMContext):
    await message.answer(
        text=ASK_CV,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(WorkState.cv)


@router.message(WorkState.cv, F.document)
async def cv_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    if message.document:
        file_data: Optional[BinaryIO] = await bot.download(file=message.document)
        file_name = f'{message.chat.id}_{message.document.file_name}'
    else:
        return

    if file_data is None:
        return

    upload_file('customers_files', file_name, file_data.read())

    await state.update_data(cv=('customers_files', file_name))

    await message.answer(
        text=ASK_CONFIRMATION,
        reply_markup=kb_from_btns(confirm_btns())
    )
    await state.set_state(WorkState.confirmation)


@router.callback_query(WorkState.confirmation, ConfirmCallback.filter())
async def confirm_handler(query: CallbackQuery, message: Message, callback_data: ConfirmCallback, bot: Bot, state: FSMContext):
    data = await state.get_data()
    application_data = {
        'Тип заявки': 'Резюме',
    }

    application = Application(
        creator_user_id=message.chat.id,  # type: ignore
        data=application_data,  # type: ignore
        files=[data['cv']]  # type: ignore
    )
    await application.save()  # type: ignore

    admins = await User.get_available()
    await spread_application_to_admins(application, admins, bot)

    await message.answer(
        text=SUCCESS_APPLICATION,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()


@router.callback_query(WorkState.confirmation, CancelCallback.filter())
async def reject_handler(query: CallbackQuery, message: Message, callback_data: CancelCallback, state: FSMContext):
    await message.answer(
        text=REJECT,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()
