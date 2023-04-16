from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message
from bot.keyboards.start import open_next_greeting_btns
from bot.keyboards.utils import kb_from_btns

from bot.messages.start import GREETING
from bot.utils.init_message import resend_init_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    
    await message.delete()
    await resend_init_message(
        message, bot, state,
        text=GREETING,
        reply_markup=kb_from_btns(open_next_greeting_btns())
    )
