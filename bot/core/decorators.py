import functools
import logging
import uuid
from asyncio import shield

from sqlalchemy.exc import DBAPIError

from core.database import create_async_session

logger = logging.getLogger(__name__)


def db_session(commit: bool = True):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            session = create_async_session()
            xid = uuid.uuid4()
            try:
                logger.debug(f'[{xid}] Transaction BEGIN;')
                result = await func(*args, **kwargs, db_session=session)
                if commit:
                    await session.commit()
                    logger.debug(f'[{xid}] Transaction COMMIT;')
            except DBAPIError as e:
                await session.rollback()
                logger.error(f'[{xid}] Transaction ROLLBACK; (Database Error)')
                raise e
            except Exception:
                await session.rollback()
                logger.error(f'[{xid}] Transaction ROLLBACK; (Application Error)')
                raise
            finally:
                if session:
                    await shield(session.close())
                    logger.debug(f'[{xid}] Connection released to pool')
            return result

        return wrapped

    return wrapper
