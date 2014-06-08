from flask.views import MethodView
from flask import render_template, g, request, redirect, url_for
from app.forms import PostForm, DeletePostForm
from app.models import Post
from flask.ext.login import login_user, logout_user,login_required
import time
import datetime
from app import db

class PostAPI(MethodView):
    decorators = [login_required]

    def get(self):
        dform = DeletePostForm()
        form = PostForm()
        user = g.user
        posts = Post.query.order_by(Post.timestamp.desc())
        return render_template('/index.html',
                title = 'Home',
                user = user,
                form = form,
                posts = posts,
                dform = dform
                )

    def post(self):
        form = PostForm(request.form)

        if form.validate_on_submit():
            content = request.form.get('body')
            print content
            currentTime = time.strftime('%Y-%m-%d-%H-%M-%S',
                    time.localtime(time.time()) )
            currentDateTime = datetime.datetime.strptime(currentTime,
                    "%Y-%m-%d-%H-%M-%S")
            user_id = g.user.id
            newPost = Post( body = content,
                    timestamp = currentDateTime,
                    user_id = user_id)

            flag = True
            try:
                db.session.add(newPost)
                db.session.commit()
            except Exception as e:
                flag = False
                db.session.rollback()
                print e
                raise e

        posts = Post.query.order_by(Post.timestamp.desc())
        dform = DeletePostForm()
        return render_template('index.html',
                title = 'Home',
                user = g.user,
                form = form,
                posts = posts,
                dform = dform
                )

    def delete(self, user_id):
        pass
