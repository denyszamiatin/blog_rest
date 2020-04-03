import os
import pathlib


BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')


class ProdConfig(Config):
    DEBUG = False
    ENV = 'production'


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False