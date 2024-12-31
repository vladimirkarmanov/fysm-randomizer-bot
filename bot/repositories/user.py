from typing import Any, Sequence

from sqlalchemy import select

from models.user import User
from repositories.base import BaseRepository
from schemas.user import UserSchema


class UserRepository(BaseRepository[User]):
    async def create(self, user: UserSchema) -> User:
        return await self.save(User(**user.__dict__))

    async def get(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        return await self.one_or_none(statement)

    async def get_all(self, limit: int, offset: int, order_by: str | None = None) -> Sequence[User]:
        statement = select(User).limit(limit).offset(offset)
        if order_by and order_by.startswith('-'):
            statement = statement.order_by(User.__table__.columns[order_by[1:]].desc())
        elif order_by:
            statement = statement.order_by(User.__table__.columns[order_by[1:]].asc())
        return await self.all(statement)

    async def update(self, user: User, **fields: dict[str, Any]) -> User:
        for field, value in fields.items():
            setattr(user, field, value)
        return await self.save(user)

    async def get_users_count(self) -> int:
        return await self.count(User) or 0
