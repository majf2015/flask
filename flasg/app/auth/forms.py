from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Username must have only letters,numbers,dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('Password2', message = 'Passwords must match.')])
    Password2 = PasswordField('Confirm Password', validators=[Required()])
    Submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise  ValidationError('Email is already register.')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise  ValidationError('Username is already use.')
