import flask
from app import db
from . import main
@main.app_errorhandler(404)
def not_found_error(error):
    return flask.render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    # This exception is triggered by a database operation
#    db.session.rollback()
    return flask.render_template('500.html'), 500

