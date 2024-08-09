import logging

from aiogram import Bot
from aiogram.types import BotCommand
from app import bot, dp


async def set_commands(bot: Bot):
    from commands.base import commands

    commands = [
        BotCommand(command=command.telegram_command, description=command.button_text) for command in commands.values()
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    logging.info('Starting connection')
    await set_commands(bot)


async def on_shutdown():
    logging.info('Bye! Shutting down connection')
    logging.info('Closing storage connection')
    await dp.storage.close()
