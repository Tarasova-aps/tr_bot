from typing import BinaryIO, Optional

from aiogram import Bot, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import (BufferedInputFile, CallbackQuery,
                           InputMediaDocument, Message)

from bot.callbacks.customer.apps_dialogs import (ConfirmDocsCallback,
                                                 ContainerTypeCallback)
from bot.callbacks.customer.complex import StartComplexCallback
from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback
from bot.keyboards.customer.apps_dialogs import (confirm_docs_btns,
                                                 container_type_btns)
from bot.keyboards.customer.confirm import confirm_btns
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.common import WAIT
from bot.messages.customer.apps_dialogs import (APPLICATION_PICKUP_DATA,
                                                ASK_CONFIRMATION, ASK_CONTACTS,
                                                ASK_CONTAINER_TYPE, ASK_DOCS,
                                                ASK_INCORRECT_WEIGHT,
                                                ASK_SPECIAL_CONDITIONS,
                                                ASK_TERMINAL,
                                                ASK_TERMINAL_DELIVERY,
                                                ASK_WAREHOUSE, ASK_WEIGHT,
                                                REJECT,
                                                SUCCESS_APPLICATION_PICKUP)
from bot.states.customer import ComplexState
from bot.utils.application import spread_application_to_admins
from models.application import Application
from models.user import User
from utils.drive import download_file, upload_file

router = Router()


@router.callback_query(StartComplexCallback.filter())
async def start_complex_handler(query: CallbackQuery, message: Message, callback_data: StartComplexCallback, state: FSMContext):
    await message.answer(
        text=ASK_CONTAINER_TYPE,
        reply_markup=kb_from_btns(container_type_btns())
    )
    await state.set_state(ComplexState.container_type)


@router.callback_query(ComplexState.container_type, ContainerTypeCallback.filter())
async def container_type_handler(query: CallbackQuery, message: Message, callback_data: ContainerTypeCallback, state: FSMContext):
    await state.update_data(container_type=callback_data.container_type)

    await message.answer(text=ASK_TERMINAL)
    await state.set_state(ComplexState.terminal)


@router.message(ComplexState.terminal, F.text)
async def terminal_handler(message: Message, state: FSMContext):
    await state.update_data(terminal=message.text)

    await message.answer(text=ASK_WAREHOUSE)
    await state.set_state(ComplexState.warehouse)


@router.message(ComplexState.warehouse, F.text)
async def warehouse_handler(message: Message, state: FSMContext):
    await state.update_data(warehouse=message.text)

    await message.answer(text=ASK_TERMINAL_DELIVERY)
    await state.set_state(ComplexState.terminal_delivery)


@router.message(ComplexState.terminal_delivery, F.text)
async def terminal_delivery_handler(message: Message, state: FSMContext):
    await state.update_data(terminal_delivery=message.text)

    await message.answer(text=ASK_WEIGHT)
    await state.set_state(ComplexState.weight)


@router.message(ComplexState.weight, F.text, F.text.as_('text'))
async def weight_handler(message: Message, text: str, state: FSMContext):
    try:
        weight = int(text)
    except ValueError:
        await message.answer(text=ASK_INCORRECT_WEIGHT)
        return

    await state.update_data(weight=weight)

    await message.answer(text=ASK_SPECIAL_CONDITIONS)
    await state.set_state(ComplexState.special_conditions)


@router.message(ComplexState.special_conditions, F.text)
async def special_conditions_handler(message: Message, state: FSMContext):
    await state.update_data(special_conditions=message.text)

    await message.answer(text=ASK_CONTACTS)
    await state.set_state(ComplexState.contacts)


@router.message(ComplexState.contacts, F.text)
async def contacts_handler(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(contacts=message.text)

    ask_docs_msg = await message.answer(
        text=ASK_DOCS(),
        reply_markup=kb_from_btns(confirm_docs_btns())
    )
    await state.update_data(ask_docs_msg_id=ask_docs_msg.message_id)

    # load and send docs
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    prices_file = BufferedInputFile(
        download_file('docs', 'prices.docx'),
        filename='prices.docx'
    )
    media_price_file = InputMediaDocument(media=prices_file)  # type: ignore

    application_file = BufferedInputFile(
        download_file('docs', 'application_complex.docx'),
        filename='application_complex.docx'
    )
    media_application_file = InputMediaDocument(media=application_file)  # type: ignore

    await bot.send_media_group(
        chat_id=message.chat.id,
        media=[media_price_file, media_application_file]
    )
    await state.update_data(docs=[])
    await state.set_state(ComplexState.docs)


@router.message(ComplexState.docs, F.photo | F.document)
async def docs_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    if message.document is not None:
        file_data: Optional[BinaryIO] = await bot.download(file=message.document)
        file_name = f'{message.chat.id}_{message.document.file_name}'
    elif message.photo is not None:
        file_data: Optional[BinaryIO] = await bot.download(file=message.photo[-1])
        file_name = f'{message.chat.id}_{message.photo[-1].file_unique_id}.png'
    else:
        return

    if file_data is None:
        return

    upload_file('customers_files', file_name, file_data.read())

    data = await state.get_data()
    data.setdefault('docs', []).append(('customers_files', file_name))
    await state.set_data(data)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data['ask_docs_msg_id'],
        text=ASK_DOCS(len(data['docs'])),
        reply_markup=kb_from_btns(confirm_docs_btns())
    )


@router.callback_query(ComplexState.docs, ConfirmDocsCallback.filter())
async def confirm_docs_handler(query: CallbackQuery, message: Message, callback_data: ConfirmDocsCallback, bot: Bot, state: FSMContext):
    data = await state.get_data()
    application_description = APPLICATION_PICKUP_DATA(
        data['container_type'],
        data['terminal'],
        data['warehouse'],
        data['terminal_delivery'],
        data['weight'],
        data['special_conditions'],
        data['contacts'],
    )

    await message.answer(
        text=ASK_CONFIRMATION + '\n' + application_description,
        reply_markup=kb_from_btns(confirm_btns())
    )
    await state.set_state(ComplexState.confirmation)


@router.callback_query(ComplexState.confirmation, ConfirmCallback.filter())
async def confirmation_handler(query: CallbackQuery, message: Message, callback_data: ConfirmDocsCallback, bot: Bot, state: FSMContext):
    await message.answer(text=WAIT)

    data = await state.get_data()
    application_data = {
        'Тип заявки': 'Запрос на прием и раскредитацию контейнера и автодоставку (комплекс)',
        'Тип контейнера': data['container_type'],
        'Терминал постановки': data['terminal'],
        'Склад': data['warehouse'],
        'Терминал сдачи': data['terminal_delivery'],
        'Вес НЕТТО (тонны)': data['weight'],
        'Специальные условия': data['special_conditions'],
        'Контакты': data['contacts'],
    }
    if message.from_user and message.from_user.username:
        application_data['Telegram'] = f'https://t.me/{message.chat.username}'

    application = Application(
        creator_user_id=message.chat.id,  # type: ignore
        data=application_data,  # type: ignore
        files=data['docs'],  # type: ignore
    )
    await application.save()  # type: ignore

    admins = await User.get_available()
    await spread_application_to_admins(application, admins, bot)

    await message.answer(
        text=SUCCESS_APPLICATION_PICKUP,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()


@router.callback_query(CancelCallback.filter())
async def cancel_handler(query: CallbackQuery, message: Message, callback_data: CancelCallback, state: FSMContext):
    await message.answer(
        text=REJECT,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()
