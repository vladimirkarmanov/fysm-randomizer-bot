import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message, CallbackQuery
from aiogram.types.error_event import ErrorEvent
from redis.asyncio.client import Redis, ConnectionPool

from errors.exceptions import InnerException
from middlewares.chat import IsPrivateUserChatMiddleware
from middlewares.chat_action import ChatActionMiddleware
from middlewares.throttling import ThrottlingMiddleware
from settings import Settings

settings = Settings()
logger = logging.getLogger('bot')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
redis_storage = RedisStorage(Redis(connection_pool=ConnectionPool(host=settings.REDIS_HOST,
                                                                  port=settings.REDIS_PORT,
                                                                  password=settings.REDIS_PASSWORD.get_secret_value())))
dp = Dispatcher(storage=redis_storage, fsm_strategy=FSMStrategy.USER_IN_CHAT)

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

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
            await bot.send_message(event.update.event.message.chat.id, f"{event.exception.msg}")
        elif isinstance(event.update.event, Message):
            await bot.send_message(event.update.message.chat.id, f"{event.exception.msg}")
        else:
            await bot.send_message(event.update.message.chat.id, f"Unhandled Event: {event.update.event}\n"
                                                                 f"exc: {event.exception.msg}")
    else:
        await bot.send_message(settings.DEVELOPER_ID, f"Ошибка!\n "
                                                      f"{event.exception.__class__}\n"
                                                      f"{event.exception}\n"
                                                      f"Message: {event.update.message.text}")


async def run_polling():
    from core.base import on_startup, on_shutdown
    from handlers import start, random
    dp.include_routers(start.router,
                       random.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot, close_bot_session=True)
    await on_shutdown()
