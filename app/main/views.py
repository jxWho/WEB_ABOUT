import flask
import time, datetime
from forms import LoginForm, RegisterForm, PostForm
from flask.ext.login import login_user, logout_user,current_user,login_required
from app import db, lm
from . import main
from ..models import User, ROLE_USER, ROLE_ADMIN, Post

@main.before_request
def before_request():
    flask.g.user = current_user

@main.route('/')
@main.route('/index')
@login_required
def index():
    user = flask.g.user
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    return flask.render_template("index.html",
            title="Home",
            user=user,
            form = form,
            posts = posts)

@main.route('/logIn', methods=['GET', 'POST'])
def login():
    if flask.g.user is not None and flask.g.user.is_authenticated():
        return flask.redirect( flask.url_for('main.index') )

    form = LoginForm()

    # If a form is posted to the server
    if form.validate_on_submit():

        Username = form.Username.data
        Password = form.Password.data
        user = User.query.filter_by(username=Username,
                password=Password).first()

        if user:
            remember_me = form.remember_me.data
            login_user(user, remember = remember_me)
            return flask.redirect(
                    flask.request.args.get('next') or
                    flask.url_for('main.index')
                    )
        else:
            flask.flash('Invalid Password or Username')
            return flask.redirect( flask.url_for('main.login') )

    return flask.render_template('login.html',
            title = "Sign In",
            form = form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        Username = User.make_unique_username( form.Username.data )
        Password = form.Password.data
        Email = form.email.data
        user = User(
                username = Username,
                email = Email,
                role = ROLE_USER,
                password = Password
                )
        db.session.add( user )
        db.session.commit()

        login_user(user)

        return flask.redirect( flask.request.args.get('next') or
                        flask.url_for('main.index')
                        )

    return flask.render_template('register.html',
            title = "Sign Up",
            form = form)

@main.route('/logout')
def logout():
    logout_user()
    return flask.redirect( flask.url_for('main.index') )

@main.route('/note')
def note():
    content = flask.request.args.get('content')
    currentTime = time.strftime('%Y-%m-%d-%H-%M-%S',
            time.localtime(time.time()) )
    currentDateTime = datetime.datetime.strptime(currentTime,
            "%Y-%m-%d-%H-%M-%S")
    user_id = flask.request.args.get('uid')
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

    if flag:
        return flask.jsonify(success=1)
    else:
        return flask.jsonify(success=0)

#Used by Flask-Login
@lm.user_loader
def load_user(id):
    return User.query.get( int(id) )


