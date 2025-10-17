import logging
import uuid
from asyncio import shield

from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.interfaces.uow import IUnitOfWork
from infra.db.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self._xid = uuid.uuid4()
        self.users = UserRepository(self.session)
        logger.debug(f'[{self._xid}] Transaction BEGIN;')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        match exc_type:
            case None:
                logger.debug(f'[{self._xid}] Transaction END;')
            case t if issubclass(t, DBAPIError):
                await self.session.rollback()
                logger.error(f'[{self._xid}] Transaction ROLLBACK; (Database Error)')
            case _:
                await self.session.rollback()
                logger.error(f'[{self._xid}] Transaction ROLLBACK; (Application Error)')

        if self.session:
            await shield(self.session.close())
            logger.debug(f'[{self._xid}] Connection released to pool')

    async def commit(self) -> None:
        await self.session.commit()
        logger.debug(f'[{self._xid}] Transaction COMMIT;')

    async def rollback(self) -> None:
        await self.session.rollback()
