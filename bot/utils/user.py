from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreateSchema, UserUpdateSchema
from services.user import UserService


async def log_user_activity(db_session: AsyncSession, id: int, username: str | None):
    await UserService(db_session).get_or_create(UserCreateSchema(id=id, username=username))
    await UserService(db_session).update(
        id=id,
        user_schema=UserUpdateSchema(username=username, last_activity_at=datetime.now()),
    )
