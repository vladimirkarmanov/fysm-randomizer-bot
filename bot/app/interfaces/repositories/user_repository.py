from abc import abstractmethod
from datetime import date
from typing import Sequence

from app.interfaces.repositories.base_repository import IBaseRepository
from domain.entities.user import User


class IUserRepository(IBaseRepository[User]):
    @abstractmethod
    async def get_active_users(self) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_active_users_count(self, dt: date) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_by_telegram_id(self, telegram_id: int) -> User | None:
        raise NotImplementedError
