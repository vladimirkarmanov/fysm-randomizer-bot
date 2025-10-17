from typing import Generic, Iterable, Sequence, Type, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repositories.base_repository import IBaseRepository

T = TypeVar('T')


class BaseSqlAlchemyRepository(IBaseRepository[T], Generic[T]):
    def __init__(self, session: AsyncSession, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    async def save(self, entity: T) -> None:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

    async def bulk_save(self, entities: Iterable) -> None:
        self.session.add_all(entities)
        for entity in entities:
            await self.session.refresh(entity)

    async def find_by_id(self, id: str) -> T | None:
        result = await self.session.execute(select(self.model_class).where(self.model_class.id == id))
        return result.scalar_one_or_none()

    async def all(self, limit: int = 100, offset: int = 0) -> Sequence[T]:
        result = await self.session.execute(select(self.model_class).limit(limit).offset(offset))
        return result.scalars().all()

    async def delete(self, id: str) -> None:
        await self.session.execute(delete(self.model_class).where(self.model_class.id == id))

    async def bulk_delete(self, ids: Iterable[str]) -> None:
        await self.session.execute(delete(self.model_class).where(self.model_class.id.in_(ids)))

    async def exists(self, id: str) -> bool:
        result = await self.session.execute(
            select(func.count()).select_from(self.model_class).where(self.model_class.id == id)
        )
        count = result.scalar_one()
        return count > 0

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model_class))
        return result.scalar_one()

    async def update(self, entity: T) -> None:
        await self.session.merge(entity)
        await self.session.flush()
        await self.session.refresh(entity)
