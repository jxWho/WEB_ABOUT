import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO= os.path.join(basedir, 'db_repository')

config = {
    'development' : DevelopmentConfig,

    'default' : DevelopmentConfig
}
