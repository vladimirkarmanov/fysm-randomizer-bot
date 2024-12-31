import logging

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_or_create(self, user: UserSchema) -> UserSchema:
        existing_user = await self.get(user.id)
        if existing_user:
            return UserSchema(**existing_user.__dict__)

        user = await self.repository.create(user)
        return user

    async def get(self, id: int) -> UserSchema | None:
        user = await self.repository.get(id)
        return UserSchema(**user.__dict__) if user else None

    async def get_all(self, limit: int, offset: int) -> list[UserSchema]:
        users = await self.repository.get_all(limit, offset)
        return [UserSchema(**u.__dict__) for u in users]

    async def get_users_count(self) -> int:
        return await self.repository.get_users_count()
