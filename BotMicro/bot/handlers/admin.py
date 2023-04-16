from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.messages.admin import ASK_ACCESS_KEY
from bot.states.admin import LoginState

from bot.utils.init_message import edit_init_message, resend_init_message

router = Router()


@router.message(Command('admin'))
async def admin_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    await resend_init_message(
        message, bot, state,
        text=ASK_ACCESS_KEY
    )    
    await state.set_state(LoginState.access_key)


@router.message(LoginState.access_key, F.text)
async def access_key_handler(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    await edit_init_message(
        message, bot, state,
        text='Ваш ключ доступа: {}'.format(message.text)
    )
