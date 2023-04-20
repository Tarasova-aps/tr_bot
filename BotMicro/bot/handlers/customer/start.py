from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.start import GREETING
from bot.utils.init_message import edit_or_resend_init_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()

    await message.delete()
    await edit_or_resend_init_message(
        message, bot, state,
        text=GREETING,
        reply_markup=kb_from_btns(open_menu_btns())
    )
