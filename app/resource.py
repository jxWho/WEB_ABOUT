import flask
from app import api
from app import app
from app.Res import Post, UserResource
from app.models import User
from flask.ext.login import login_user, logout_user,current_user,login_required

api.add_resource(Post.PostRe, '/post')
api.add_resource(UserResource.userResource, '/user')



@app.route('/user/login', methods=['POST'])
def ulogin():
    Username = flask.request.form["Username"]
    Password = flask.request.form["Password"]

    user = User.query.filter_by(
            username = Username,
            password = Password
            ).first()

    if user:
        login_user(user, remember=False)
        return flask.jsonify(
                    success = 1,
                    uid = user.id
                )
    else:
        return flask.jsonify(
                    success = 0
                )
