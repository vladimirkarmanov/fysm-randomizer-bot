from datetime import date
from typing import Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.interfaces.repositories.user_repository import IUserRepository
from domain.entities.user import User
from infra.db.repositories.base_sqlalchemy_repository import BaseSqlAlchemyRepository


class UserRepository(BaseSqlAlchemyRepository[User], IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_active_users(self, dt: date) -> Sequence[User]:
        result = await self.session.execute(
            select(User).filter(func.date(User.last_activity_at) == dt).order_by(desc(User.last_activity_at))
        )
        return result.scalars().all()

    async def get_active_users_count(self, dt: date) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model_class).filter(func.date(User.last_activity_at) == dt)
        )
        return result.scalar_one()

    async def find_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(self.model_class).filter_by(telegram_id=telegram_id))
        return result.scalars().first()
