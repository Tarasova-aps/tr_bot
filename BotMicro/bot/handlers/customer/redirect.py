from aiogram import Bot, Router
from aiogram.filters import Filter
from aiogram.types import Message

from bot.keyboards.hide_message import hide_message_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.redirect import SUCCESS
from bot.utils.admins import forward_message_to_admins
from models.user import User

router = Router()


class NotAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        attached_admins = await User.query(User.chat_id == message.chat.id)  # type: ignore
        if attached_admins:
            return False

        return True


@router.message(NotAdminFilter())
async def redirect_handler(message: Message, bot: Bot):
    await forward_message_to_admins(bot, message)
    await message.reply(
        text=SUCCESS,
        reply_markup=kb_from_btns(hide_message_btns())
    )
