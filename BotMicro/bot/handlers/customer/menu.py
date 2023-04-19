from aiogram import Router

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.customer.menu import OpenMenuCallback
from bot.keyboards.customer.complex import start_complex_btns
from bot.keyboards.customer.apps_dialogs import start_container_pickup_btns
from bot.keyboards.customer.docs import open_info_btns
from bot.keyboards.customer.partnership import start_partnership_btns
from bot.keyboards.customer.website import website_btns
from bot.keyboards.customer.work import start_work_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.menu import TITLE

router = Router()


@router.callback_query(OpenMenuCallback.filter())
async def open_menu_handler(query: CallbackQuery, message: Message, callback_data: OpenMenuCallback, state: FSMContext):
    await message.answer(
        text=TITLE,
        reply_markup=kb_from_btns(
            start_container_pickup_btns(),
            start_complex_btns(),
            start_partnership_btns(),
            start_work_btns(),
            open_info_btns(),
            website_btns()
        )
    )
    await state.clear()
