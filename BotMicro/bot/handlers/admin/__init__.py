from aiogram import Router

from .login import router as admin_router

router = Router()
router.include_router(admin_router)
