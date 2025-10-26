import logging.config
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisEventIsolation, RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand, CallbackQuery, Message
from aiogram.types.error_event import ErrorEvent
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from app.exceptions import InnerException
from infra.config.settings import get_settings
from infra.container import container
from infra.db.models import start_sqlalchemy_mappers
from telegram.middleware.chat import IsPrivateUserChatMiddleware
from telegram.middleware.chat_action import ChatActionMiddleware
from telegram.middleware.throttling import ThrottlingMiddleware

settings = get_settings()


LOGGING: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
}
if settings.DEBUG:
    LOGGING['root']['level'] = 'DEBUG'
    LOGGING['formatters'] = {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(name)-30s %(yellow)s%(message)s',
        }
    }
    LOGGING['handlers'] = {
        'console': {
            'class': 'colorlog.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'colored',
        },
    }

logging.config.dictConfig(LOGGING)


bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
bot_redis_storage = RedisStorage(
    redis=Redis(
        connection_pool=ConnectionPool(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD.get_secret_value()
        )
    ),
    key_builder=DefaultKeyBuilder(with_destiny=True),
)
dp = Dispatcher(
    storage=bot_redis_storage,
    events_isolation=RedisEventIsolation(redis=bot_redis_storage.redis),
    fsm_strategy=FSMStrategy.USER_IN_CHAT,
    di=container,
)


if settings.is_prod:
    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

dp.message.middleware(IsPrivateUserChatMiddleware())
dp.callback_query.middleware(IsPrivateUserChatMiddleware())
dp.message.middleware(ChatActionMiddleware())
dp.callback_query.middleware(ChatActionMiddleware())


@dp.errors()
async def default_error_handler(event: ErrorEvent):
    if isinstance(event.exception, InnerException):
        if isinstance(event.update.event, CallbackQuery):
            await bot.send_message(event.update.event.message.chat.id, f'{event.exception.msg}')
        elif isinstance(event.update.event, Message):
            await bot.send_message(event.update.message.chat.id, f'{event.exception.msg}')
        else:
            await bot.send_message(
                event.update.message.chat.id, f'Unhandled Event: {event.update.event}\nexc: {event.exception.msg}'
            )
    else:
        await bot.send_message(
            settings.DEVELOPER_ID,
            f'Ошибка!\n {event.exception.__class__}\n{event.exception}\nMessage: {event.update.message.text}',
        )


async def set_commands(bot: Bot):
    from constants.commands import side_menu

    commands = [
        BotCommand(command=command.telegram_command, description=command.button_text) for command in side_menu.values()
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    logging.info('Starting connection')
    await set_commands(bot)
    start_sqlalchemy_mappers()


async def on_shutdown():
    logging.info('Bye! Shutting down connection')
    logging.info('Closing storage connection')
    await dp.storage.close()


async def run_polling():
    from handlers import feedback, start
    from handlers.admin import router as admin_router
    from handlers.random import router as random_router

    dp.include_routers(start.router, feedback.router, random_router.router, admin_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot, close_bot_session=True)
    await on_shutdown()
