from flask import render_template, request, url_for, redirect, flash, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from secrets import token_urlsafe
from app import app, db
from app.models import User, Video
import os

@app.route('/temporary/<path:filename>')
def temporary(filename):
  return send_from_directory(app.config['TEMP_FOLDER'], filename)

@app.route('/')
#@app.route('/index')
def index():
  videos = Video.query.all()
  return render_template('index.html', videos=videos)

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
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    error = False
    if User.query.filter_by(email=email).first() is not None:
      flash('Please, use a different email.')
      error = True
    elif User.query.filter_by(username=username).first() is not None:
      flash('Please, use a different username.')
      error = True
    if error:
      return redirect(url_for('register'))
    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash('Welcome to PyTube :)')
    return redirect(url_for('login'))

  return render_template('register.html')

def allowed_file(filename):
  return '.' in filename and filename.split('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if request.method == 'POST':
    video_file = request.files.get('video_file')
    title = request.form.get('title')
    description = request.form.get('description')

    if not allowed_file(video_file.filename):
      flash('Submit a valid video file: *.webm only!')
      return redirect(url_for('upload'))

    valid_url = False
    while not valid_url:
      watch_id = token_urlsafe(7)
      valid_url = Video.query.filter_by(watch_id=watch_id).first() is None

    video = Video(watch_id=watch_id, author=current_user, title=title, description=description, binary=video_file.read())
    db.session.add(video)
    db.session.commit()
    return redirect(url_for('index'))

  return render_template('upload.html')

@app.route('/user_profile')
@login_required
def user_profile():
  return render_template('user_profile.html')

@app.route('/watch')
def watch():
  watch_id = request.args.get('v')
  video = Video.query.filter_by(watch_id=watch_id).first()
  video_file = url_for('temporary', filename=f'{watch_id}.webm')
  with open(os.path.join('app', app.config['TEMP_FOLDER'], f'{watch_id}.webm'), 'wb') as f:
    f.write(video.binary)

  return render_template('watch.html', video_file=video_file, video=video)

@app.route('/user_profile/configure', methods=['GET', 'POST'])
@login_required
def configure():
  if request.method == 'POST':
    actual_password = request.form.get('actual_password')
    password = request.form.get('password')
    
    if not current_user.check_password(actual_password):
      return redirect(request.url)
    
    current_user.set_password(password)
    db.session.commit()

    logout_user()
    return redirect(url_for('login'))

  return render_template('configure.html')

@app.route('/search')
def search():
  search = request.args.get('s')
  print(search)
  videos = Video.query.all()
  return render_template('search.html', search=search, videos=videos)
