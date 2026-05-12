import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _get_database_url():
    """
    Determine the correct database URL.
    Tests PostgreSQL connectivity before committing to it.
    Falls back to SQLite if PostgreSQL is unavailable.
    """
    database_url = os.getenv('DATABASE_URL')

    if database_url:
        # Fix legacy postgres:// prefix
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)

        # Test if PostgreSQL is actually reachable before using it
        try:
            import psycopg2
            from urllib.parse import urlparse
            parsed = urlparse(database_url)
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                dbname=parsed.path.lstrip('/'),
                user=parsed.username,
                password=parsed.password,
                connect_timeout=5
            )
            conn.close()
            print(f"✓ PostgreSQL connection verified")
            return database_url
        except Exception as e:
            print(f"⚠ PostgreSQL unavailable ({e}), falling back to SQLite")

    # SQLite fallback — use absolute path so it always works
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getenv('RENDER'):
        sqlite_path = 'sqlite:////opt/render/project/src/nexora.db'
    else:
        db_dir = os.path.join(base_dir, 'instance')
        os.makedirs(db_dir, exist_ok=True)
        sqlite_path = f'sqlite:///{os.path.join(db_dir, "nexora.db")}'

    print(f"✓ Using SQLite: {sqlite_path}")
    return sqlite_path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'nexora-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'nexora-jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    SQLALCHEMY_DATABASE_URI = _get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,   # test connection before using it
        'pool_recycle': 300,     # recycle connections every 5 minutes
    }

    UPLOAD_FOLDER = '/opt/render/project/src/uploads' if os.getenv('RENDER') else 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MODEL_PATH = 'ml/model.pkl'
    VECTORIZER_PATH = 'ml/vectorizer.pkl'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
