from app import db, login
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    videos = db.relationship('Video', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    binary = db.Column(db.LargeBinary)
    title = db.Column(db.String(140))
    description = db.Column(db.String(600), default="")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Video {}>'.format(self.title)   


@login.user_loader
def load_user(id):
  return User.query.get(int(id))