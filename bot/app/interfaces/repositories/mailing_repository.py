from app.interfaces.repositories.base_repository import IBaseRepository
from domain.entities.mailing import Mailing


class IMailingRepository(IBaseRepository[Mailing]):
    pass
