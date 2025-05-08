from typing import Sequence

from sqlalchemy import select

from models.mailing import Mailing
from repositories.base import BaseRepository
from schemas.mailing import MailingCreateSchema


class MailingRepository(BaseRepository[Mailing]):
    async def create(self, user: MailingCreateSchema) -> Mailing:
        return await self.save(Mailing(**user.__dict__))

    async def get(self, id: int) -> Mailing | None:
        statement = select(Mailing).where(Mailing.id == id)
        return await self.one_or_none(statement)

    async def get_all(self, limit: int, offset: int, order_by: str | None = None) -> Sequence[Mailing]:
        statement = select(Mailing).limit(limit).offset(offset)
        if order_by and order_by.startswith('-'):
            statement = statement.order_by(Mailing.__table__.columns[order_by[1:]].desc())
        elif order_by:
            statement = statement.order_by(Mailing.__table__.columns[order_by[1:]].asc())
        return await self.all(statement)
