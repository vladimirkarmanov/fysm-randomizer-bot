from aiogram import Router

# from handlers.admin.mailing import router as mailing_router
from handlers.admin.panel import router as panel_router
from handlers.admin.users import router as users_router

from infra.config.settings import get_settings
from telegram.middleware.auth import IsAdminMiddleware

router = Router(name='admin')
settings = get_settings()

if settings.is_prod:
    router.message.middleware.register(IsAdminMiddleware())
    router.callback_query.middleware.register(IsAdminMiddleware())

router.include_routers(
    panel_router,
    users_router,
    # mailing_router,
)
