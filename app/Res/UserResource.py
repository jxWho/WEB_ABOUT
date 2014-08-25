from flask.ext.restful import Resource
from app.models import User
import flask

class userResource(Resource):
    def get(self):
        users = User.query.all()
        UserArray = []
        for user in users:
            userDic = {}
            userDic["id"] = user.id
            userDic['username'] = user.username
            userDic['password'] = user.password

            UserArray.append( userDic )

        return flask.jsonify( users = UserArray )
    pass
