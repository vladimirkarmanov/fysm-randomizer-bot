import logging
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.mailing import MailingRepository
from schemas.mailing import MailingCreateSchema, MailingGetSchema

logger = logging.getLogger(__name__)


class MailingService:
    def __init__(self, session: AsyncSession):
        self.repository = MailingRepository(session)

    async def create(self, mailing: MailingCreateSchema) -> MailingGetSchema:
        return await self.repository.create(mailing)

    async def get(self, id: int) -> MailingGetSchema | None:
        mailing = await self.repository.get(id)
        return MailingGetSchema(**mailing.__dict__) if mailing else None

    async def get_all(self, limit: int, offset: int, order_by: str | None = None) -> Sequence[MailingGetSchema]:
        mailing_list = await self.repository.get_all(limit, offset, order_by)
        return [MailingGetSchema(**m.__dict__) for m in mailing_list]
