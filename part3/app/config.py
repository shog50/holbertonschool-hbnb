import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
