import os
import sqlite3

from core.migrations import apply_alembic_migrations
from settings import settings

BOT_ABS_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_PATH = os.path.normpath(os.path.join(os.path.dirname(BOT_ABS_PATH), 'fixtures'))


def ensure_database_exists():
    with sqlite3.connect(os.path.join(BOT_ABS_PATH, settings.DATABASE_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT SQLITE_VERSION()')
        data = cursor.fetchone()
        print('SQLite version:', data)


ensure_database_exists()
apply_alembic_migrations(verbose=settings.DEBUG)
