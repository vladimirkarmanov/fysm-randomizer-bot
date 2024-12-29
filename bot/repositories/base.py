from typing import Generic, TypeVar

from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Select, Update

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def add_all(self, objs: list) -> None:
        self.session.add_all(objs)

    async def one_or_none(self, statement: Select) -> T | None:
        return (await self.session.execute(statement)).scalars().one_or_none()

    async def all(self, statement: Select) -> list[T]:
        return (await self.session.execute(statement)).scalars().all()

    async def _all(self, statement: Select) -> list[T]:
        return (await self.session.execute(statement)).all()

    async def execute(self, statement: Select | Update | Delete) -> CursorResult:
        return await self.session.execute(statement)
