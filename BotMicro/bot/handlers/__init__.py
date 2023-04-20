from os import getenv

from aiogram import Router

from .admin import router as admin_router
from .customer import router as customer_router
from .error import router as error_router
from .hide_message import router as hide_message_router

router = Router()
router.include_router(hide_message_router)
router.include_router(admin_router)
router.include_router(customer_router)

if getenv('ENABLE_ERRORS_LOGS') == 'True':
    router.include_router(error_router)
