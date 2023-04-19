from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.menu import OpenMenuCallback
from bot.keyboards.complex import start_complex_btns
from bot.keyboards.container_pickup import start_container_pickup_btns
from bot.keyboards.docs import open_docs_btns
from bot.keyboards.partnership import start_partnership_btns
from bot.keyboards.utils import kb_from_btns
from bot.keyboards.website import website_btns
from bot.keyboards.work import start_work_btns
from bot.messages.customer.menu import TITLE
from bot.utils.init_message import edit_init_message

router = Router()


@router.callback_query(OpenMenuCallback.filter())
async def open_menu_handler(query: CallbackQuery, message: Message, callback_data: OpenMenuCallback, bot: Bot, state: FSMContext):
    await edit_init_message(
        message, bot, state,
        text=TITLE,
        reply_markup=kb_from_btns(
            start_container_pickup_btns(),
            start_complex_btns(),
            start_partnership_btns(),
            start_work_btns(),
            open_docs_btns(),
            website_btns()
        )
    )
    await state.clear()
