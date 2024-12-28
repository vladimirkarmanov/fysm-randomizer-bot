import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create(self, user: UserSchema) -> UserSchema:
        user = await self.repository.create(**user.__dict__)
        return user

    async def get(self, id: int) -> UserSchema:
        user = await self.repository.get(id)
        return UserSchema(**user.__dict__)

    async def get_all(self, limit: int, offset: int) -> list[UserSchema]:
        users = await self.repository.get_all(limit, offset)
        return [UserSchema(**u.__dict__) for u in users]

    async def update(self, id: int, **fields: dict[str, Any]):
        pass
