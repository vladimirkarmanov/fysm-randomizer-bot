from typing import Any

from sqlalchemy import select

from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def create(self, user: User) -> User:
        return await self.save(user)

    async def get(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        return await self.one_or_none(statement)

    async def get_all(self, limit: int, offset: int) -> list[User]:
        statement = select(User).limit(limit).offset(offset)
        return await self.all(statement)

    async def update(self, user: User, **fields: dict[str, Any]) -> User:
        for field, value in fields.items():
            setattr(user, field, value)
        return await self.save(user)
