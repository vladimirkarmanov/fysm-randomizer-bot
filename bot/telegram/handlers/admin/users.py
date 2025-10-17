from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters.command import Command
from callbacks.pagination import PaginationCallback
from constants.commands import admin
from formatters.formatter import entity_to_str
from schemas.keyboard import ButtonSchema
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message

from infra.config.settings import get_settings
from ioc import IoC

router = Router()
settings = get_settings()


@router.message(Command(admin['users'].command))
@router.message(F.text == admin['users'].button_text)
async def get_users(
    message: types.Message,
    ioc: IoC,
):
    async with ioc.uow:
        users = await ioc.uow.users.all(limit=settings.ITEMS_PER_PAGE, offset=0)
        total_users = await ioc.uow.users.count()

    text = '\n\n'.join([entity_to_str(u) for u in users])

    buttons = []
    if total_users > settings.ITEMS_PER_PAGE:
        buttons.append(
            ButtonSchema(
                text='➡️', callback_data=PaginationCallback(callback_name='next', offset=settings.ITEMS_PER_PAGE)
            )
        )

    await message.answer(
        text=f'Пользователи ({len(users)}/{total_users}):\n\n{text}',
        parse_mode='HTML',
        reply_markup=get_inline_keyboard(buttons, row_size=2),
    )


@router.callback_query(PaginationCallback.filter(F.callback_name == 'prev'))
@router.callback_query(PaginationCallback.filter(F.callback_name == 'next'))
async def next_users(
    callback: types.CallbackQuery,
    callback_data: PaginationCallback,
    ioc: IoC,
):
    offset = callback_data.offset
    async with ioc.uow:
        users = await ioc.uow.users.all(limit=settings.ITEMS_PER_PAGE, offset=offset)
        total_users = await ioc.uow.users.count()

    text = '\n\n'.join([entity_to_str(u) for u in users])

    buttons = []
    if offset != 0:
        buttons.append(
            ButtonSchema(
                text='⬅️',
                callback_data=PaginationCallback(callback_name='prev', offset=offset - settings.ITEMS_PER_PAGE),
            )
        )

    if total_users > offset + settings.ITEMS_PER_PAGE:
        buttons.append(
            ButtonSchema(
                text='➡️',
                callback_data=PaginationCallback(callback_name='next', offset=offset + settings.ITEMS_PER_PAGE),
            )
        )

    await update_text_message(
        message=callback.message,
        new_value=f'Пользователи ({offset + len(users)}/{total_users}):\n\n{text}',
        keyboard=get_inline_keyboard(buttons, row_size=2),
    )
    await callback.answer()


@router.message(Command(admin['activity'].command))
@router.message(F.text == admin['activity'].button_text)
async def get_activity(
    message: types.Message,
    ioc: IoC,
):
    async with ioc.uow:
        dt = datetime.now().date()
        users_count = await ioc.uow.users.get_active_users_count(dt)

    await message.answer(
        text=f'<b>{datetime.now().date()}</b>\nАктивных пользователей: {users_count}',
        reply_markup=None,
    )
