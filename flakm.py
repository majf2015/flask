from flask import Flask, render_template, current_app, g, request, session, redirect, url_for, flash
import flask
import os
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Message, Mail


class NameForm(Form):
    name = StringField('what is your name?', validators = [Required(), Length(min = 1, max = 20)])
    role = StringField('what is your role?', validators = [Required(), Length(min = 1, max = 20)])
    submit = SubmitField('Submit')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)
app.config['SECRET_KEY'] = 'secret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/python/myproject/venv/flask/sqlitef.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/myproject/venv/flask/sqlitef.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin<1102103123@qq.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    user_introduction = db.Column(db.String(64), default = 'default')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Role %r>' % self.username

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data.lower()).first()
        role = Role.query.filter_by(name = form.role.data.lower()).first()
        if user is None:
            if role is None:
                user_role = Role(name = form.role.data.lower())
                user = User(username = form.name.data.lower(), role = user_role)
            else:
                user = User(username = form.name.data.lower(), role = role)
            db.session.add(user)
            session['know'] = False
            #if app.config['FLASKY_ADMIN']:
             #   send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user = user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(),
                           form = form, name = session.get('name'), know = session.get('know', False))


@app.route('/redirect')
def redirect_hello():
    return redirect('http://127.0.0.1:5000/')

@app.route('/user/<name>')
def user(name):
    mydict = {'key' : 'mydicttest', 'value' : 'keyvalue'}
    mylist = ['listtest', 'mylisttest']
    return render_template('username.html',name = name, mydict = mydict, mylist = mylist)

@app.route('/bootstrap')
def strap():
    return render_template('bootstrap.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role)
manager.add_command('shell', Shell(make_context = make_shell_context))

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subjest, sender =app.config['FLASKY_MAIL_SENDER'],
                  recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    mail.send(msg)



if __name__ == '__main__':
    manager.run()
