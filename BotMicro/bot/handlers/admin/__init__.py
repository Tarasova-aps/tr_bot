from aiogram import Router

from .login import router as admin_router
from .menu import router as menu_router
from .users import router as users_router
from .application import router as application_router

router = Router()
router.include_router(admin_router)
router.include_router(menu_router)
router.include_router(users_router)
router.include_router(application_router)
