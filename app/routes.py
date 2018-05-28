from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', videos=range(13))

@app.route('/user_profile')
def user_profile():
  return render_template('user_profile.html')
