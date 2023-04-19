from aiogram import Router

from .complex import router as complex_router
from .container_pickup import router as container_pickup_router
from .docs import router as docs_router
from .menu import router as menu_router
from .partnership import router as partnership_router
from .start import router as start_router
from .work import router as work_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(container_pickup_router)
router.include_router(complex_router)
router.include_router(partnership_router)
router.include_router(work_router)
router.include_router(docs_router)
