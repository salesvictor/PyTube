from app import app
from flask import render_template
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def generic_error(error):
  code = 500
  desc = '<p>Something occurred, the administrators have already been notified!</p>'
  if isinstance(error, HTTPException):
    code = error.code
    desc = error.get_description()
  desc = desc[3:-4]
  return render_template('error.html', error=code, desc=desc), code
