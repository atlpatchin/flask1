from flask import Flask,render_template,session,redirect,url_for,flash
from flask import request
from flask import make_response
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms import StringField,SubmitField
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Shell
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.mail import Mail,Message
basedir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
manager.add_command('db',MigrateCommand)
app.config['SQLALCHEMY_DATABASE_URI'] =\
         'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER']='smtp.163.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='atlpat@163.com'
app.config['MAIL_PASSWORD']='llh151'
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <atlpat@163.com>'
def send_email(to,subject,template,**kwargs):
    msg= Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    mail.send(msg)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.config['SECRET_KEY']='hard go guess string'
mail=Mail(app)
class NameForm(Form):
    name = StringField('What is you name?',validators=[Required()])
    submit = SubmitField('Submit')
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    def __repr__(self):
        return '<Role %r>' %self.name

    users = db.relationship('User',backref='role',lazy = 'dynamic')
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    def __repr__(self):
        return '<User %r>' %self.username
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
     #  old_name = session.get('name')
      # if old_name is not None and old_name!=form.name.data:
       #    flash('Looks like you have changed your name!')

        #name = form.name.data
       user = User.query.filter_by(username = form.name.data).first()
       if user is None:

         user = User(username=form.name.data)
         db.session.add(user)
         session['known'] = False
         if app.config['FLASKY_ADMIN']:
            send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
       else:

         session['known']=True
       session['name']=form.name.data
       form.name.data=''

       return redirect(url_for('index'))

    return render_template('index.html',known=session.get('known',False),current_time=datetime.utcnow(),form=form,name=session.get('name'))
    #response = make_response('<h1>this document carries a cookies!<h1>')
    #response.set_cookie('answer','42')
   # return response
    #user_agent = request.headers.get('User-Agent')
    #return '<p>Your brower is %s</p>' %user_agent
   # return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello,%s!<h1>'%name
    return render_template('user.html',name=name)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
if __name__=='__main__':
    manager.run()
