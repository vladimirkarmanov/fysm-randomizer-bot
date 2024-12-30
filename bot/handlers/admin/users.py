from aiogram import F, Router, types
from aiogram.filters.command import Command
from sqlalchemy.ext.asyncio import AsyncSession

from constants.commands import admin
from core.decorators import db_session
from services.user import UserService

router = Router()


@router.message(Command(admin['users'].command))
@router.message(F.text == admin['users'].button_text)
@db_session(commit=False)
async def get_users(message: types.Message, *, db_session: AsyncSession):
    users = await UserService(db_session).get_all(limit=100, offset=0)
    text = '\n\n'.join([str(u.__dict__) for u in users])
    await message.answer(text=f'Пользователи:\n{text}', parse_mode='HTML')
