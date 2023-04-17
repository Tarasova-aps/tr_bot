from aiogram import Router

from .container_pickup import router as container_pickup_router
from .menu import router as menu_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(container_pickup_router)
