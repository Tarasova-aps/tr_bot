from os import getenv

from aiogram import Router

from .docs import router as docs_router
from .error import router as error_router
from .menu import router as menu_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(docs_router)

if getenv('ENABLE_ERRORS_LOGS') == 'True':
    router.include_router(error_router)
