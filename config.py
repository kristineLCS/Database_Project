import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Ensure DATABASE_URL is set
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
assert SQLALCHEMY_DATABASE_URI, "DATABASE_URL must be set in the environment variables"

# Base configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
