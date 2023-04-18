from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.customer.confirm import CancelCallback, ConfirmCallback
from bot.callbacks.customer.partnership import StartPartnershipCallback
from bot.keyboards.customer.confirm import confirm_btns
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.apps_dialogs import (APPLICATION_PARTNERSHIP_DATA,
                                                ASK_CONFIRMATION, ASK_CONTACTS,
                                                ASK_PARTNERSHIP_OFFER, REJECT,
                                                SUCCESS_APPLICATION)
from bot.states.customer import PartnershipState
from bot.utils.application import spread_application_to_admins
from models.application import Application
from models.user import User

router = Router()


@router.callback_query(StartPartnershipCallback.filter())
async def start_partnership_handler(query: CallbackQuery, message: Message, callback_data: StartPartnershipCallback, state: FSMContext):
    await message.answer(
        text=ASK_PARTNERSHIP_OFFER,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(PartnershipState.partnership_offer)


@router.message(PartnershipState.partnership_offer, F.text)
async def partnership_offer_handler(message: Message, state: FSMContext):
    await state.update_data(partnership_offer=message.text)

    await message.answer(
        text=ASK_CONTACTS(None),
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.set_state(PartnershipState.contacts)


@router.message(PartnershipState.contacts, F.text)
async def contacts_handler(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)

    data = await state.get_data()
    application_description = APPLICATION_PARTNERSHIP_DATA(
        data['partnership_offer'],
        data['contacts'],
    )
    await message.answer(
        text=ASK_CONFIRMATION + '\n' + application_description,
        reply_markup=kb_from_btns(confirm_btns())
    )
    await state.set_state(PartnershipState.confirmation)


@router.callback_query(PartnershipState.confirmation, ConfirmCallback.filter())
async def confirm_handler(query: CallbackQuery, message: Message, callback_data: ConfirmCallback, bot: Bot, state: FSMContext):
    data = await state.get_data()
    application_data = {
        'Тип заявки': 'Предложение о сотрудничестве',
        'Предложение': data['partnership_offer'],
        'Контакты': data['contacts'],
    }

    application = Application(
        creator_user_id=message.chat.id,  # type: ignore
        data=application_data,  # type: ignore
    )
    await application.save()  # type: ignore

    admins = await User.get_available()
    await spread_application_to_admins(application, admins, bot)

    await message.answer(
        text=SUCCESS_APPLICATION,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()


@router.callback_query(PartnershipState.confirmation, CancelCallback.filter())
async def cancel_handler(query: CallbackQuery, message: Message, callback_data: CancelCallback, state: FSMContext):
    await message.answer(
        text=REJECT,
        reply_markup=kb_from_btns(open_menu_btns())
    )
    await state.clear()
