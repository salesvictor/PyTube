from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', videos=range(13))

@app.route('/404')
def error404():
  return render_template('404.html')

@app.route('/auth')
def auth():
  return render_template('auth.html')
