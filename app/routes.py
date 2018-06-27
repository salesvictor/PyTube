from flask import render_template
from app import app
from app.forms import LoginForm

user = None # not authenticated forced

@app.route('/')
#@app.route('/index')
def index():
  return render_template('index.html', videos=range(13), user=user)

@app.route('/login')
def login():
  form = LoginForm()
  return render_template('login.html', form=form)
