from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repositories.mailing_repository import IMailingRepository
from domain.entities.mailing import Mailing
from infra.db.repositories.base_sqlalchemy_repository import BaseSqlAlchemyRepository


class MailingRepository(BaseSqlAlchemyRepository[Mailing], IMailingRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Mailing)
