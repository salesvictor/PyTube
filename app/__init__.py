import os
import logging
from flask import Flask
from config import Config
from pathlib import Path
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

if not app.debug:
  if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
       auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
      secure = ()
    mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                               fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                               toaddrs=app.config['ADMINS'], subject='PyTube Failure',
                               credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

  os.makedirs('logs', exist_ok=True)
  file_handler = RotatingFileHandler(Path('logs/pytube.log'), maxBytes=10485760, backupCount=10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)

  app.logger.setLevel(logging.INFO)
  app.logger.info('PyTube Startup')

from app import routes, errors
