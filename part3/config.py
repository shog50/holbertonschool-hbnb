import os
from datetime import timedelta

class Config:
    # Basic App Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-key-456')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
