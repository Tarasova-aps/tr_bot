from aiogram import Bot, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import (BufferedInputFile, CallbackQuery,
                           InputMediaDocument, Message)

from bot.callbacks.customer.docs import OpenDocsCallback
from bot.keyboards.customer.menu import open_menu_btns
from bot.keyboards.utils import kb_from_btns
from bot.messages.customer.menu import TITLE
from utils.drive import download_file

router = Router()


@router.callback_query(OpenDocsCallback.filter())
async def start_container_pickup_handler(query: CallbackQuery, message: Message, callback_data: OpenDocsCallback, bot: Bot, state: FSMContext):
    await message.answer(
        text=TITLE,
        reply_markup=kb_from_btns(open_menu_btns())
    )

    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    
    pickup_application_file = BufferedInputFile(
        download_file('docs', 'application_pickup.doc'),
        filename='application_pickup.doc'
    )
    media_pickup_application_file = InputMediaDocument(media=pickup_application_file)  # type: ignore

    complex_application_file = BufferedInputFile(
        download_file('docs', 'application_complex.docx'),
        filename='application_complex.docx'
    )
    media_complex_application_file = InputMediaDocument(media=complex_application_file)  # type: ignore

    disagreements_file = BufferedInputFile(
        download_file('docs', 'disagreements.doc'),
        filename='disagreements.doc'
    )
    media_disagreements_file = InputMediaDocument(media=disagreements_file)  # type: ignore

    prices_file = BufferedInputFile(
        download_file('docs', 'prices.docx'),
        filename='prices.docx'
    )
    media_prices_file = InputMediaDocument(media=prices_file)  # type: ignore

    await message.answer_media_group(
        media=[
            media_pickup_application_file,
            media_complex_application_file,
            media_disagreements_file,
            media_prices_file
        ]
    )
