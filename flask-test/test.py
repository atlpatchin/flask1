
from flask import redirect
from flask import Flask
from flask.ext.script import Manager
from flask.ext.moment import Moment

app = Flask(__name__)
manager=Manager(app)
moment =Moment(app)
@app.route('/')
def index():
    return redirect('http://www.example.com')
#from flask import abort
#@app.route('/user/<id>')
#def get_user(id):
    #user = load_user(id)
    #if not user:
    #    abort(404)
   # return '<h1>hello, %s</h1>' %user.name
if __name__=='__main__':
 #   app.run(debug=True)
    manager.run()
