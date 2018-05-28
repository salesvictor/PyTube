from flask import render_template
from app import app

user = None # not authenticated forced

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', videos=range(13), user=user)

@app.route('/user_profile')
def user_profile():
  # TODO: Handle authentication logic
  if user == None:
    return render_template('auth.html')
  else:
    return render_template('user_profile.html')
