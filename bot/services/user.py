import logging
from datetime import date
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserCreateSchema, UserGetSchema, UserUpdateSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_or_create(self, user: UserCreateSchema) -> UserGetSchema:
        existing_user = await self.get(user.id)
        if existing_user:
            return UserGetSchema(**existing_user.__dict__)

        user = await self.repository.create(user)
        return user

    async def get(self, id: int) -> UserGetSchema | None:
        user = await self.repository.get(id)
        return UserGetSchema(**user.__dict__) if user else None

    async def get_all(self, limit: int, offset: int, order_by: str | None = None) -> Sequence[UserGetSchema]:
        users = await self.repository.get_all(limit, offset, order_by)
        return [UserGetSchema(**u.__dict__) for u in users]

    async def get_active_users(self, dt: date) -> Sequence[UserGetSchema]:
        users = await self.repository.get_active_users(dt)
        return [UserGetSchema(**u.__dict__) for u in users]

    async def get_users_count(self) -> int:
        return await self.repository.get_users_count()

    async def update(self, id: int, user_schema: UserUpdateSchema):
        user = await self.repository.get(id)
        await self.repository.update(user, **user_schema.__dict__)
