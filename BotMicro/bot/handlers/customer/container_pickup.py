from typing import BinaryIO, Optional

from aiogram import Bot, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import (BufferedInputFile, CallbackQuery,
                           InputMediaDocument, Message)

from bot.callbacks.customer.apps_dialogs import (ConfirmDocsCallback,
                                                 SkipContactsCallback)
from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback
from bot.callbacks.customer.container_pickup import \
    StartContainerPickupCallback
from bot.keyboards.customer.apps_dialogs import (confirm_docs_btns,
                                                 skip_contacts_btns)
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
                                                REJECT, SUCCESS_APPLICATION)
from bot.states.customer import ContainerPickupState
from bot.utils.application import spread_application_to_admins
from models.application import Application
from models.user import User
from utils.drive import download_file, upload_file

router = Router()


@router.callback_query(StartContainerPickupCallback.filter())
async def start_container_pickup_handler(query: CallbackQuery, message: Message, callback_data: StartContainerPickupCallback, state: FSMContext):
    await message.answer(
        text=ASK_CONTAINER_TYPE,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.container_type)


@router.message(ContainerPickupState.container_type, F.text)
async def container_type_handler(message: Message, state: FSMContext):
    await state.update_data(container_type=message.text)

    await message.answer(
        text=ASK_TERMINAL,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.terminal)


@router.message(ContainerPickupState.terminal, F.text)
async def terminal_handler(message: Message, state: FSMContext):
    await state.update_data(terminal=message.text)

    await message.answer(
        text=ASK_WAREHOUSE,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.warehouse)


@router.message(ContainerPickupState.warehouse, F.text)
async def warehouse_handler(message: Message, state: FSMContext):
    await state.update_data(warehouse=message.text)

    await message.answer(
        text=ASK_TERMINAL_DELIVERY,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.terminal_delivery)


@router.message(ContainerPickupState.terminal_delivery, F.text)
async def terminal_delivery_handler(message: Message, state: FSMContext):
    await state.update_data(terminal_delivery=message.text)

    await message.answer(
        text=ASK_WEIGHT,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.weight)


@router.message(ContainerPickupState.weight, F.text, F.text.as_('text'))
async def weight_handler(message: Message, text: str, state: FSMContext):
    try:
        weight = int(text)
    except ValueError:
        await message.answer(
            text=ASK_INCORRECT_WEIGHT,
            reply_markup=kb_from_btns(open_menu_btns())
        )
        return

    await state.update_data(weight=weight)

    await message.answer(
        text=ASK_SPECIAL_CONDITIONS,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(ContainerPickupState.special_conditions)


@router.message(ContainerPickupState.special_conditions, F.text)
async def special_conditions_handler(message: Message, state: FSMContext):
    await state.update_data(special_conditions=message.text)

    btns = [skip_contacts_btns(), open_menu_btns()] if message.chat.username else [open_menu_btns()]
    await message.answer(
        text=ASK_CONTACTS(message.chat.username),
        reply_markup=kb_from_btns(*btns)
    )
    await state.set_state(ContainerPickupState.contacts)


@router.callback_query(SkipContactsCallback.filter())
async def skip_contacts_handler(query: CallbackQuery, message: Message, callback_data: SkipContactsCallback, bot: Bot, state: FSMContext):
    await contacts_handler(message, bot, state)
    await state.update_data(contacts='')


@router.message(ContainerPickupState.contacts, F.text)
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
        download_file('docs', 'application_pickup.doc'),
        filename='application_pickup.doc'
    )
    media_application_file = InputMediaDocument(media=application_file)  # type: ignore

    await bot.send_media_group(
        chat_id=message.chat.id,
        media=[media_price_file, media_application_file]
    )
    await state.update_data(docs=[])
    await state.set_state(ContainerPickupState.docs)


@router.message(ContainerPickupState.docs, F.photo | F.document)
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


@router.callback_query(ContainerPickupState.docs, ConfirmDocsCallback.filter())
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
    await state.set_state(ContainerPickupState.confirmation)


@router.callback_query(ContainerPickupState.confirmation, ConfirmCallback.filter())
async def confirmation_handler(query: CallbackQuery, message: Message, callback_data: ConfirmDocsCallback, bot: Bot, state: FSMContext):
    await message.answer(
        text=WAIT,
        reply_markup=kb_from_btns(open_menu_btns())
    )

    data = await state.get_data()
    application_data = {
        'Тип заявки': 'Запрос на автовывоз контейнера',
        'Тип контейнера': data['container_type'],
        'Терминал постановки': data['terminal'],
        'Склад': data['warehouse'],
        'Терминал сдачи': data['terminal_delivery'],
        'Вес НЕТТО (тонны)': data['weight'],
        'Специальные условия': data['special_conditions'],
        'Контакты': data['contacts'],
    }
    if message.chat.username:
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
        text=SUCCESS_APPLICATION,
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
