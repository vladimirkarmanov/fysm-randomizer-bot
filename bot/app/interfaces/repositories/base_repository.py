from abc import ABC, abstractmethod
from typing import Generic, Iterable, Sequence, TypeVar

T = TypeVar('T')


class IBaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_save(self, entities: Iterable[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str | int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, limit: int = 100, offset: int = 0) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str | int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_delete(self, ids: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, id: str | int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> None:
        raise NotImplementedError
