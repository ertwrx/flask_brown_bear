import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration class."""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Flask configuration
    DEBUG = False
    TESTING = False
    
    # Database configuration
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + str(BASE_DIR / 'app.db'))
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Application settings
    APP_NAME = os.environ.get('APP_NAME', 'Brown Bear App')
    
    # File paths
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration."""
    # Production should always use environment variables for sensitive config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI')
    
    # Ensure these are set in production
    def __init__(self):
        assert self.SECRET_KEY, "SECRET_KEY environment variable must be set in production"
        assert self.DATABASE_URI, "DATABASE_URI environment variable must be set in production"


# Configuration dictionary to easily access different configs
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Function to get configuration based on environment
def get_config():
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])
