from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.customer.start import (OpenAboutUsCallback,
                                          OpenContactsCallback)
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.customer.start import open_about_us_btns, open_contacts_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.start import ABOUT_US, CONTACTS, GREETING
from bot.utils.init_message import edit_init_message, resend_init_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()

    await message.delete()
    await resend_init_message(
        message, bot, state,
        text=GREETING,
        reply_markup=kb_from_btns(open_about_us_btns())
    )


@router.callback_query(OpenAboutUsCallback.filter())
async def open_about_us_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await query.answer()

    await edit_init_message(
        message, bot, state,
        text=ABOUT_US,
        reply_markup=kb_from_btns(open_contacts_btns())
    )


@router.callback_query(OpenContactsCallback.filter())
async def open_contacts_handler(query: CallbackQuery, message: Message, bot: Bot, state: FSMContext):
    await query.answer()

    await edit_init_message(
        message, bot, state,
        text=CONTACTS,
        reply_markup=kb_from_btns(open_menu_btns())
    )
