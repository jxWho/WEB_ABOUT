import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask_wtf.csrf import CsrfProtect
from flask.ext.restful import Api
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from config import config

csrf = CsrfProtect()

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
lm = LoginManager()
lm.login_view = 'main.login'
api = Api()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    csrf.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    lm.init_app(app)
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app




