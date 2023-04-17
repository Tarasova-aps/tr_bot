from asyncio import gather
from typing import Optional

from aiogram import Bot
from aiogram.types import BufferedInputFile

from bot.keyboards.admin.application import hide_application_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.admin.application import APPLICATION_NOTIFY
from models.application import Application
from models.user import User
from utils.drive import download_file


async def send_application_to_admin(
    application: Application,
    chat_id: int,
    bot: Bot,
    files: Optional[list[BufferedInputFile]] = None
) -> None:
    await bot.send_message(
        chat_id=chat_id,
        text=APPLICATION_NOTIFY(application),
        reply_markup=kb_from_btns(
            hide_application_btns(app_key=application.app_key)
        )
    )
    if files is None:
        return
    
    for file in files:
        await bot.send_document(
            chat_id=chat_id,
            document=file,
        )


async def spread_application_to_admins(
    application: Application,
    admins: list[User],
    bot: Bot,
) -> None:
    files_data = {
        file[1]: download_file(file[0], file[1])
        for file in application.files
    }
    files = [
        BufferedInputFile(data, filename=name)
        for name, data in files_data.items()
    ]

    await gather(
        *[
            send_application_to_admin(
                application=application,
                chat_id=admin.chat_id,
                bot=bot,
                files=files
            )
            for admin in admins if admin.chat_id
        ],
        return_exceptions=False
    )
