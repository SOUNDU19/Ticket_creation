import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database
    AVIAN_CONNECTION_STRING = os.getenv('AVIAN_CONNECTION_STRING', None)
    # Use /tmp for Vercel serverless (ephemeral storage)
    db_path = os.getenv('DATABASE_URL', '/tmp/nexora.db' if os.getenv('VERCEL') else 'sqlite:///instance/nexora.db')
    SQLALCHEMY_DATABASE_URI = db_path if db_path.startswith('sqlite:///') or db_path.startswith('postgresql://') else f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS - Allow Vercel frontend and local development
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8000,https://ticket-creation-c1xe.vercel.app,https://*.vercel.app')
    
    # Upload
    UPLOAD_FOLDER = '/tmp/uploads' if os.getenv('VERCEL') else 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # ML Models
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
