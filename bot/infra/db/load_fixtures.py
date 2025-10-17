import os

import psycopg2

BOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_PATH = os.path.normpath(os.path.join(BOT_DIR, 'fixtures'))


def load_fixtures() -> None:
    fixtures = [
        os.path.join(FIXTURES_PATH, f)
        for f in os.listdir(FIXTURES_PATH)
        if os.path.isfile(os.path.join(FIXTURES_PATH, f))
    ]
    for fixture in fixtures:
        with open(fixture, 'r') as f:
            sql = f.read()
            try:
                conn = psycopg2.connect(os.getenv('SYNC_DATABASE_URL'))
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                print('Fixtures loaded successfully')
            except Exception as exc:
                print(f'Exception |{exc}| occured during loading fixtures')
                conn.rollback()
            finally:
                conn.close()


if __name__ == '__main__':
    load_fixtures()
