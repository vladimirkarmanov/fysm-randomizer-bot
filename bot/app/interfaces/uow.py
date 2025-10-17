from abc import ABC, abstractmethod

from app.interfaces.repositories.user_repository import IUserRepository


class IUnitOfWork(ABC):
    users: IUserRepository

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
