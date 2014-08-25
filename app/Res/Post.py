from flask.ext.restful import Resource
from app.models import Post
import flask

class PostRe(Resource):
    def get(self):
        posts = Post.query.order_by( Post.timestamp.desc() )
        postArray = []
        for post in posts:
            tempDic = {}
            tempDic['body'] = post.body
            tempDic['timestamp'] = post.timestamp
            postArray.append( tempDic )
            print post.body
            pass
        print 'call'
        return flask.jsonify(posts = postArray)
