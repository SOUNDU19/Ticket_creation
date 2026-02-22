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
    # Use absolute path for database
    if os.getenv('RENDER'):
        # On Render, use /opt/render/project/src for persistent storage
        SQLALCHEMY_DATABASE_URI = 'sqlite:////opt/render/project/src/nexora.db'
    else:
        # Local development
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/nexora.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS - Allow Vercel frontend and local development
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000,https://ticket-creation-c1xe.vercel.app,https://*.vercel.app').split(',')
    
    # Upload
    UPLOAD_FOLDER = '/opt/render/project/src/uploads' if os.getenv('RENDER') else 'uploads'
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
