from aiogram import F, Router, types
from aiogram.filters.command import Command
from sqlalchemy.ext.asyncio import AsyncSession

from constants.commands import admin
from core.decorators import db_session
from services.user import UserService
from utils.formatter import schema_obj_to_str

router = Router()


@router.message(Command(admin['users'].command))
@router.message(F.text == admin['users'].button_text)
@db_session(commit=False)
async def get_users(message: types.Message, *, db_session: AsyncSession):
    user_service = UserService(db_session)
    users = await user_service.get_all(limit=100, offset=0)
    total_users = await user_service.get_users_count()

    text = '\n\n'.join([schema_obj_to_str(u) for u in users])
    await message.answer(text=f'Пользователи ({total_users}):\n{text}', parse_mode='HTML')
