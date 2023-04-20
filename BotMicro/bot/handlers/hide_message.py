from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.hide_message import HideMessageCallback

router = Router()


@router.callback_query(HideMessageCallback.filter())
async def hide_message_handler(query: CallbackQuery, message: Message, callback_data: HideMessageCallback, bot: Bot, state: FSMContext):
    await message.delete()
    await state.clear()
