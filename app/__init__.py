import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
import config

configs = {
    'dev': config.DevConfig,
    'prod': config.ProdConfig,
}

app = Flask(__name__)
app.config.from_object(configs.get(os.getenv('APP_CONFIG'), config.ProdConfig))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from . import controllers
