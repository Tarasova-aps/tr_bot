from typing import BinaryIO, Optional

from aiogram import Bot, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback
from bot.callbacks.customer.container_pickup import \
    StartContainerPickupCallback
from bot.callbacks.customer.container_type import ContainerTypeCallback
from bot.callbacks.customer.docs import ConfirmDocs
from bot.keyboards.customer.confirm import confirm_btns
from bot.keyboards.customer.container_pickup import container_type_btns
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.container_pickup import (APPLICATION_PICKUP_DATA,
                                                    ASK_CONFIRMATION,
                                                    ASK_CONTAINER_TYPE,
                                                    ASK_DOCS,
                                                    ASK_DOCS_CONFIRMATION,
                                                    ASK_INCORRECT_WEIGHT,
                                                    ASK_SPECIAL_CONDITIONS,
                                                    ASK_TERMINAL,
                                                    ASK_TERMINAL_DELIVERY,
                                                    ASK_WAREHOUSE, ASK_WEIGHT,
                                                    REJECT,
                                                    SUCCESS_APPLICATION_PICKUP)
from bot.messages.customer.customer_contacts import ASK_EMAIL
from bot.states.customer import ContainerPickupState
from bot.utils.application import spread_application_to_admins
from bot.utils.init_message import edit_init_message, update_init_message
from models.application import Application
from models.user import User
from utils.drive import download_file, upload_file

router = Router()


@router.callback_query(StartContainerPickupCallback.filter())
async def start_container_pickup_handler(query: CallbackQuery, message: Message, callback_data: StartContainerPickupCallback, bot: Bot, state: FSMContext):
    await update_init_message(
        message, state,
        text=ASK_DOCS,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    prices_file = BufferedInputFile(download_file('docs', 'prices.docx'), filename='prices.docx')
    application_file = BufferedInputFile(
        download_file('docs', 'application_pickup.doc'),
        filename='application_pickup.doc'
    )

    docs_messages: list[int] = []
    msg = await bot.send_document(
        chat_id=message.chat.id,
        document=prices_file
    )
    docs_messages.append(msg.message_id)
    msg = await bot.send_document(
        chat_id=message.chat.id,
        document=application_file
    )
    docs_messages.append(msg.message_id)

    await state.set_state(ContainerPickupState.docs)
    await state.update_data(docs_messages=docs_messages)


@router.message(ContainerPickupState.docs, F.photo | F.document)
@router.message(ContainerPickupState.docs_confirmation, F.photo | F.document)
async def docs_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    if message.document is not None:
        file_data: Optional[BinaryIO] = await bot.download(file=message.document)
        file_name = str(message.chat.id) + '_' + str(message.document.file_name)
    elif message.photo is not None:
        file_data: Optional[BinaryIO] = await bot.download(file=message.photo[-1])
        file_name = str(message.chat.id) + '_' + message.photo[-1].file_unique_id + '.png'
    else:
        return

    if not file_data:
        return

    upload_file('customers_files', file_name, file_data.read())

    data = await state.get_data()
    data.setdefault('docs', []).append(('customers_files', file_name))
    await state.set_data(data)

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_DOCS_CONFIRMATION,
        reply_markup=kb_from_btns(confirm_btns())
    )

    await state.set_state(ContainerPickupState.docs_confirmation)


@router.callback_query(ContainerPickupState.docs_confirmation, ConfirmCallback.filter())
async def confirm_docs_handler(query: CallbackQuery, message: Message, callback_data: ConfirmDocs, bot: Bot, state: FSMContext):
    data = await state.get_data()
    for msg_id in data['docs_messages']:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        except:
            pass

    await update_init_message(
        message, state,
        text=ASK_CONTAINER_TYPE,
        reply_markup=kb_from_btns(
            container_type_btns(),
            open_menu_btns()
        )
    )

    await state.set_state(ContainerPickupState.container_type)


@router.callback_query(ContainerTypeCallback.filter())
async def container_type_handler(query: CallbackQuery, message: Message, callback_data: ContainerTypeCallback, bot: Bot, state: FSMContext):
    container_type = callback_data.container_type

    await update_init_message(
        message, state,
        text=ASK_TERMINAL,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.update_data(container_type=container_type)
    await state.set_state(ContainerPickupState.terminal)


@router.message(ContainerPickupState.terminal, F.text)
async def terminal_handler(message: Message, bot: Bot, state: FSMContext):
    terminal = message.text

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_WAREHOUSE,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.update_data(terminal=terminal)
    await state.set_state(ContainerPickupState.warehouse)


@router.message(ContainerPickupState.warehouse, F.text)
async def warehouse_handler(message: Message, bot: Bot, state: FSMContext):
    warehouse = message.text

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_TERMINAL_DELIVERY,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.update_data(warehouse=warehouse)
    await state.set_state(ContainerPickupState.terminal_delivery)


@router.message(ContainerPickupState.terminal_delivery, F.text)
async def terminal_delivery_handler(message: Message, bot: Bot, state: FSMContext):
    terminal_delivery = message.text

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_WEIGHT,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.update_data(terminal_delivery=terminal_delivery)
    await state.set_state(ContainerPickupState.weight)


@router.message(ContainerPickupState.weight, F.text, F.text.as_('text'))
async def weight_handler(message: Message, bot: Bot, text: str, state: FSMContext):
    try:
        weight = int(text)
    except ValueError:
        await message.delete()
        await edit_init_message(
            message, bot, state,
            text=ASK_INCORRECT_WEIGHT,
            reply_markup=kb_from_btns(
                open_menu_btns()
            )
        )
        return

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_SPECIAL_CONDITIONS,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.update_data(weight=weight)
    await state.set_state(ContainerPickupState.special_conditions)


@router.message(ContainerPickupState.special_conditions, F.text)
async def special_conditions_handler(message: Message, bot: Bot, state: FSMContext):
    special_conditions = message.text
    await state.update_data(special_conditions=special_conditions)

    data = await state.get_data()
    app_data = APPLICATION_PICKUP_DATA(
        data['container_type'],
        data['terminal'],
        data['warehouse'],
        data['terminal_delivery'],
        data['weight'],
        data['special_conditions'],
    )

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=ASK_CONFIRMATION + '\n' + app_data,
        reply_markup=kb_from_btns(confirm_btns())
    )

    await state.set_state(ContainerPickupState.confirmation)


@router.callback_query(ContainerPickupState.confirmation, ConfirmCallback.filter())
async def confirm_handler(query: CallbackQuery, message: Message, callback_data: ConfirmCallback, bot: Bot, state: FSMContext):
    await update_init_message(
        message, state,
        text=ASK_EMAIL,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )
    await state.set_state(ContainerPickupState.email)


@router.callback_query(CancelCallback.filter())
async def cancel_handler(query: CallbackQuery, message: Message, callback_data: CancelCallback, bot: Bot, state: FSMContext):
    await update_init_message(
        message, state,
        text=REJECT,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.clear()


@router.message(ContainerPickupState.email, F.text)
async def email_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    email = message.text

    application_data = {
        'Тип контейнера': data['container_type'],
        'Терминал постановки': data['terminal'],
        'Склад': data['warehouse'],
        'Терминал сдачи': data['terminal_delivery'],
        'Вес НЕТТО (тонны)': data['weight'],
        'Специальные условия': data['special_conditions'],
        'Email': email,
    }
    if message.from_user and message.from_user.username:
        application_data['Telegram'] = f'https://t.me/{message.from_user.username}'

    application = Application(
        creator_user_id=message.chat.id,  # type: ignore
        data=application_data,  # type: ignore
        files=data['docs'],  # type: ignore
    )
    await application.save()  # type: ignore

    admins = await User.get_available()
    await spread_application_to_admins(application, admins, bot)

    await message.delete()
    await edit_init_message(
        message, bot, state,
        text=SUCCESS_APPLICATION_PICKUP,
        reply_markup=kb_from_btns(
            open_menu_btns()
        )
    )

    await state.clear()
