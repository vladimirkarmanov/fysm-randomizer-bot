from aiogram import Router

from handlers.admin.base import router as base_router
from middlewares.auth import IsAdminMiddleware
from settings import settings

router = Router(name='admin')

if settings.is_prod:
    router.message.middleware.register(IsAdminMiddleware())
    router.callback_query.middleware.register(IsAdminMiddleware())

router.include_routers(base_router)
