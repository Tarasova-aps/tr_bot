from asyncio import gather
from typing import Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message

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


async def forward_message_to_admins(bot: Bot, message: Message):
    admin = await User.get_available()
    await gather(*[
        bot.forward_message(
            chat_id=admin.chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        for admin in admin if admin.chat_id
    ])
