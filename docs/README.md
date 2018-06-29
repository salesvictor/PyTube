# PyTube
PyTube is a simple and unpretentious project for a video streaming web platform, at the models of Youtube, focused on a interesting and practical use of the [Flask](http://flask.pocoo.org/) framework for Python. 
Most of the project was directly based on [The Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

### File Structure
```
.
├── app
│   ├── errors.py
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   └── img
│   ├── templates
│   ├── temporary
│   └── thumbnail.py
├── app.db
├── config.py
├── docs
├── logs
├── migrations
├── Pipfile
├── Pipfile.lock
└── pytube.py
```
## Setting up the code
The following instructions are based on Linux (Ubuntu >= 16.04) setup for localhosting of the web application project.

### Prerequisites
First, install ```Python3.6``` (previous versions may not work easily, as we use the new [secrets](https://docs.python.org/3/library/secrets.html) module for generating video url). Then, install ```pip``` and ```pipenv``` for packages and virtual enviroment management. 

Then install the following dependencies at your virtual enviroment:
* [Flask](http://flask.pocoo.org/)
* [Flask-WTF](https://pythonhosted.org/Flask-WTF/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
* [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
* [Flask-Login](https://flask-login.readthedocs.io/)

All these flask dependencies needed are set in the Pipfile configuration for pipenv. Additionaly, you must install the following dependencies for image processing (applied in the thumbinailing code):
* [Pillow](https://pillow.readthedocs.io/en/5.1.x/installation.html)
* [PyAv](https://mikeboers.github.io/PyAV/installation.html)
* [ffmpeg](https://www.ffmpeg.org/)


## Authors

* **Victor Sales** - [salesvictor](https://github.com/salesvictor)
* **Diego Pereira** - [diegotbl](https://github.com/diegotbl)
* **Juan Freire** - [juanfdg](https://github.com/juanfdg)

## Acknowledgments

* **Professor Edgar Toshiro Yano** - [Curriculum](http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4798593T1&idiomaExibicao=2)

