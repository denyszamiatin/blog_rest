import os
import pathlib


BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    ITEMS_ON_PAGE = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1@localhost:5432/postgres"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "dev_data" / "db.sqlite3")


class TestConfig(Config):
    DEBUG = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
