from flask import url_for
from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  videos = db.relationship('Video', backref='author', lazy='dynamic')
  posts = db.relationship('Post', backref='author', lazy='dynamic')
 
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<User {}>'.format(self.username)

class Video(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  watch_id = db.Column(db.String(20), index=True, unique=True) 
  binary = db.Column(db.LargeBinary)
  title = db.Column(db.String(140))
  description = db.Column(db.String(600), default="")
  thumbnail = db.Column(db.LargeBinary)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  views = db.Column(db.Integer, default=0)
  posts = db.relationship('Post', backref='video', lazy='dynamic')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  def get_thumbnail(self):
    thumbnail_path = os.path.join('app', app.config['TEMP_FOLDER'], f'{self.watch_id}.jpg')
    with open(thumbnail_path, 'wb') as f:
      f.write(self.thumbnail)

    return url_for('temporary', filename='{}.jpg'.format(self.watch_id))
  def __repr__(self):
    return '<Video {}>'.format(self.title)   

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(160))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

class Watched(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  video_id = db.Column(db.Integer)
