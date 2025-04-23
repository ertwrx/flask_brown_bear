import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration class."""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')

    # Flask configuration
    DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 't')
    TESTING = False

    # Database configuration (if used)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + str(BASE_DIR / 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # Application settings
    APP_NAME = os.environ.get('APP_NAME', 'Brown Bear App')

    # Static file handling
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

    # Security headers
    STRICT_TRANSPORT_SECURITY = os.environ.get('STRICT_TRANSPORT_SECURITY', 'false').lower() in ('true', '1', 't')
    CONTENT_SECURITY_POLICY = os.environ.get('CONTENT_SECURITY_POLICY')

    # Normalize database path
    raw_db_uri = os.environ.get('DATABASE_URI')
    if raw_db_uri and raw_db_uri.startswith('sqlite:///') and not raw_db_uri.startswith('sqlite:////'):
        # Add full absolute path if needed
        db_path = BASE_DIR / raw_db_uri.replace('sqlite:///', '')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.resolve()}"
    else:
        SQLALCHEMY_DATABASE_URI = raw_db_uri or f"sqlite:///{(BASE_DIR / 'instance/app.db').resolve()}"


    # Ensure basic validation - these should be set in production
    def validate(self):
        """Validate critical configuration values."""
        if os.environ.get('FLASK_ENV') == 'production':
            assert self.SECRET_KEY != 'dev-key-please-change-in-production', \
                "Production requires a real SECRET_KEY environment variable"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'app.db')  # Use absolute path here


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration."""
    def __init__(self):
        super().validate()


# Configuration dictionary to easily access different configs
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the appropriate configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'default')
    return config[env]()  # Return an instance of the config class
