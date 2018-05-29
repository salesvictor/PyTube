import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'pytube-eh-toppern'
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = ['salesrvictor@gmail.com', 'juanfdantas@gmail.com', 'diegoblima2010@gmail.com']
