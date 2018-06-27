from flask import render_template, request
from app import app
# from app import db
# from app.models import Video

user = None # not authenticated forced

@app.route('/')
#@app.route('/index')
def index():
  return render_template('index.html', videos=range(13), user=user)

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    # video_file = request.files['video_file']
    # video = Video(user=user, name=video_file.filename, data=video_file.read())
    # db.session.add(video)
    # db.session.commit()
    return redirect(url_for('index'))

  return render_template('upload.html')
