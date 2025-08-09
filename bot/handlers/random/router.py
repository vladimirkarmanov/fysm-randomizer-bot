from aiogram import Router

from handlers.random.base import router as base_router
from handlers.random.dense import router as dense_router
from handlers.random.grand import router as grand_router
from handlers.random.mortal import router as mortal_router
from handlers.random.random import router as random_router

router = Router(name='random')
router.include_routers(random_router, base_router, dense_router, grand_router, mortal_router)
