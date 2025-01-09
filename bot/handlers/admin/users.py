from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters.command import Command
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.pagination import PaginationCallback
from constants.commands import admin
from core.decorators import db_session
from schemas.keyboard import ButtonSchema
from services.user import UserService
from settings import settings
from utils.formatter import schema_obj_to_str
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message

router = Router()


@router.message(Command(admin['users'].command))
@router.message(F.text == admin['users'].button_text)
@db_session(commit=False)
async def get_users(message: types.Message, *, db_session: AsyncSession):
    user_service = UserService(db_session)
    users = await user_service.get_all(limit=settings.ITEMS_PER_PAGE, offset=0, order_by='-created_at')
    total_users = await user_service.get_users_count()
    text = '\n\n'.join([schema_obj_to_str(u) for u in users])

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
@db_session(commit=False)
async def next_users(
    callback: types.CallbackQuery,
    callback_data: PaginationCallback,
    *,
    db_session: AsyncSession,
):
    offset = callback_data.offset
    user_service = UserService(db_session)
    users = await user_service.get_all(limit=settings.ITEMS_PER_PAGE, offset=offset, order_by='-created_at')
    total_users = await user_service.get_users_count()
    text = '\n\n'.join([schema_obj_to_str(u) for u in users])

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
@db_session(commit=False)
async def get_activity(message: types.Message, *, db_session: AsyncSession):
    user_service = UserService(db_session)
    users = await user_service.get_active_users(dt=datetime.now().date())
    text = '\n\n'.join([f'{schema_obj_to_str(u)}' for u in users])

    await message.answer(
        text=f'Активность ({datetime.now().date()}):\n\n{text}',
        parse_mode='HTML',
        reply_markup=None,
    )
