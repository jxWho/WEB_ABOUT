from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField, PasswordField \
                    ,TextAreaField
import wtforms
from wtforms.validators import Required, Length, EqualTo

class LoginForm(Form):
    Username = TextField('Username',
                validators = [Required(),Length(min=1, max=64)]
                )
    Password = PasswordField('Password',
            validators = [Required(), Length(min=6, max=20)]
            )
    remember_me = BooleanField('remember_me', default=False)
    submit_button = SubmitField('Sign In')

class RegisterForm(Form):
    Username = TextField('Username',
                validators = [Required(), Length(min=1, max=64)]
            )
    Password = PasswordField('Password',
                validators = [Required(),
                    Length(min=4, max=64),
                    EqualTo('confirm', message="Passwords must match")]
            )
    confirm = PasswordField('Repeat Password')
    email = TextField('Email Address',
            validators = [
                Length(min=7, max=35),
                wtforms.validators.Email(
                    'The format of the Email is incorrect')
                ]
            )
    submit_button = SubmitField('Sign up')

class PostForm(Form):
    body = TextAreaField('Content',
            validators=[Required(), Length(min=2, max=140)]
            )

    submit_button = SubmitField('Post')
