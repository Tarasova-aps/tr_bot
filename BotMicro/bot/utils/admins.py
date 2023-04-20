from asyncio import gather
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from typing import Optional

from models.user import User


async def spread_message_to_admins(bot: Bot, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
    admin = await User.get_available()
    await gather(*[
        bot.send_message(
            chat_id=admin.chat_id,
            text=text,
            reply_markup=reply_markup
        )
        for admin in admin if admin.chat_id
    ])
