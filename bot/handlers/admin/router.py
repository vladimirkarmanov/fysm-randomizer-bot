from aiogram import Router

from handlers.admin.panel import router as panel_router
from handlers.admin.users import router as users_router
from middlewares.auth import IsAdminMiddleware
from settings import settings

router = Router(name='admin')

if settings.is_prod:
    router.message.middleware.register(IsAdminMiddleware())
    router.callback_query.middleware.register(IsAdminMiddleware())

router.include_routers(panel_router, users_router)
