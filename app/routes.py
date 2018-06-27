from flask import render_template, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import app
from app.models import User

user = None # not authenticated forced

@app.route('/')
#@app.route('/index')
def index():
  return render_template('index.html', videos=range(13), user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
      flash('Invalid username or password')
      return redirect(url_for('login'))

    login_user(user, remember=request.form.get('remember-me'))
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      return redirect(url_for('index'))
    return redirect(next_page)

  return render_template('login.html')

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  if request.method == 'POST':
    email = requet.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    error = False
    if User.query.filter_by(email=email).first() is not None:
      flash('Please, use a different email.')
      error = True
    if User.query.filter_by(username=username).first() is not None:
      flash('Please, use a different username.')
      error = True
    if error:
      redirect(url_for('register'))
    
    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash('Welcome to PyTube :)')
    return redirect(url_for('index'))
 
  return render_template('register.html')
