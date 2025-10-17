import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from infra.config.settings import Settings, get_settings

logger = logging.getLogger(__name__)


def create_engines(settings: Settings) -> tuple[Engine, AsyncEngine]:
    sync_engine: Engine = create_engine(settings.SYNC_DATABASE_URL)
    async_engine: AsyncEngine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

    logging.info('Engines are created.')
    # TODO: сделать dispose engine
    # sync_engine.dispose()
    # async_engine.dispose()
    # logging.info("Engine is disposed.")
    return sync_engine, async_engine


def create_sessionmakers(
    engine: Engine, async_engine: AsyncEngine
) -> tuple[sessionmaker[Session], async_sessionmaker[AsyncSession]]:
    create_session = sessionmaker(bind=engine, expire_on_commit=False)
    create_async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    return create_session, create_async_session


engine, async_engine = create_engines(get_settings())
session_factory, async_session_factory = create_sessionmakers(engine, async_engine)
