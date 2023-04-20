from aiogram import Router

from .callback import router as callback_router
from .docs import router as docs_router
from .menu import router as menu_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(docs_router)
router.include_router(callback_router)
