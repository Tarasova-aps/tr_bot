from aiogram import Router

from .login import router as admin_router
from .menu import router as menu_router

router = Router()
router.include_router(admin_router)
router.include_router(menu_router)
