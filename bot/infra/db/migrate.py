import logging
import os
import sys

from alembic import command
from alembic.config import Config

from infra.config.settings import get_settings

logger = logging.getLogger(__name__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_PATH = os.path.normpath(os.path.join(DB_FOLDER_PATH, 'alembic'))
ALEMBIC_INI_PATH = os.path.normpath(os.path.join(PROJECT_ROOT, 'alembic.ini'))
# FIXTURES_PATH = os.path.normpath(os.path.join(os.path.dirname(DB_FOLDER_PATH), 'fixtures'))


def write_to_stderr(chars: str):
    sys.stderr.write(chars + '\n')


def apply_alembic_migrations(verbose: bool = False) -> None:
    separate = '-' * 60
    separate_short = '-' * 22
    logger.info('Applying migrations')
    write_to_stderr(f'{separate_short}Alembic history:{separate_short}')
    config = Config(ALEMBIC_INI_PATH, stdout=sys.stderr)
    config.set_main_option('script_location', ALEMBIC_PATH)
    command.history(config)
    write_to_stderr(separate)
    write_to_stderr(f'{separate_short}Alembic upgrade:{separate_short}')
    command.upgrade(config, 'head')
    command.current(config, verbose=verbose)
    write_to_stderr(separate)


apply_alembic_migrations(verbose=get_settings().DEBUG)
