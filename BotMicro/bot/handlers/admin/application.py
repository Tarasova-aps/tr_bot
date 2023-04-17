from aiogram import Router
from aiogram.types import CallbackQuery, Message

from bot.callbacks.admin.applications import HideApplicationCallback

router = Router()


@router.callback_query(HideApplicationCallback.filter())
async def hide_application_handler(query: CallbackQuery, message: Message, callback_data: HideApplicationCallback):
    await message.delete()
