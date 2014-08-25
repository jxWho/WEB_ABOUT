import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask_wtf.csrf import CsrfProtect
from flask.ext.restful import Api

csrf = CsrfProtect()

app = Flask(__name__)
db = SQLAlchemy(app)
Bootstrap(app)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#csrf.init_app(app)

api = Api(app)


from app import views, models, resource



