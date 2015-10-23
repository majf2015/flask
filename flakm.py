from flask import Flask, render_template, current_app, g, request, session, redirect, url_for, flash
import flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length



class NameForm(Form):
    name = StringField('what is your name?', validators = [Required(), Length(min = 10, max = 20)])
    submit = SubmitField('Submit')


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'secret'

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have change your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(), form = form, name = session.get('name'))


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



if __name__ == '__main__':
    manager.run()
