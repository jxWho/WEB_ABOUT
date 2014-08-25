import flask
import time, datetime
from app import app
from forms import LoginForm, RegisterForm, PostForm
from flask.ext.login import login_user, logout_user,current_user,login_required
from app import app, db, lm
from models import User, ROLE_USER, ROLE_ADMIN, Post

@app.before_request
def before_request():
    flask.g.user = current_user

@app.errorhandler(404)
def not_found_error(error):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # This exception is triggered by a database operation
    db.session.rollback()
    return flask.render_template('500.html'), 500

@app.route('/')
@app.route('/index')
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

@app.route('/logIn', methods=['GET', 'POST'])
def login():
    if flask.g.user is not None and flask.g.user.is_authenticated():
        return flask.redirect( flask.url_for('/index') )

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
                    flask.url_for('index')
                    )
        else:
            flask.flash('Invalid Password or Username')
            return flask.redirect( flask.url_for('login') )

    return flask.render_template('login.html',
            title = "Sign In",
            form = form)

@app.route('/register', methods=['GET', 'POST'])
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
                        flask.url_for('index')
                        )

    return flask.render_template('register.html',
            title = "Sign Up",
            form = form)

@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect( flask.url_for('index') )

@app.route('/note')
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


