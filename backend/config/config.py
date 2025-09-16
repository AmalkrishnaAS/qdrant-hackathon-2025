import os
from decouple import config
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = config('SECRET_KEY', default='dev-secret-key-change-in-production')
    DEBUG = config('DEBUG', default=True, cast=bool)
    

    # Qdrant Configuration
    QDRANT_HOST = config('QDRANT_HOST', default='localhost')
    QDRANT_PORT = config('QDRANT_PORT', default=6333, cast=int)
    QDRANT_API_KEY = config('QDRANT_API_KEY', default=None)
    QDRANT_COLLECTION_NAME = config('QDRANT_COLLECTION_NAME', default='youtube_audio_embeddings')

    # Upstash Configuration (optional)
    UPSTASH_REDIS_REST_URL = config('UPSTASH_REDIS_REST_URL', default=None)
    UPSTASH_REDIS_REST_TOKEN = config('UPSTASH_REDIS_REST_TOKEN', default=None)

    # Celery Configuration (optional)
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
    # File Upload Configuration
    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default='uploads')
    MAX_CONTENT_LENGTH = config('MAX_CONTENT_LENGTH', default=100 * 1024 * 1024, cast=int)  # 100MB
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mp3', 'wav', 'jpg', 'jpeg', 'png', 'gif'}

    # API Configuration
    API_TITLE = 'Music Video Processing API'
    API_VERSION = 'v1'
    API_DESCRIPTION = 'Backend API for music video processing with AI-powered recommendations'

    # CORS Configuration
    CORS_ORIGINS = config('CORS_ORIGINS', default='http://localhost:3000,http://localhost:3001').split(',')
    CORS_HEADERS = ['Content-Type','x-access-token']
    CORS_SUPPORTS_CREDENTIALS = True
    # Embedding Model Configuration
    SENTENCE_TRANSFORMER_MODEL = config('SENTENCE_TRANSFORMER_MODEL', default='all-MiniLM-L6-v2')
    
    # AI Service API Keys
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', default=None)
    
    # CLAP Model Configuration
    CLAP_MODEL_NAME = config('CLAP_MODEL_NAME', default='laion/clap-htsat-unfused')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}