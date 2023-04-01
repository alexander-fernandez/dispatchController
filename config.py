"""Flask configuration."""
from os import path

basedir = path.abspath(path.dirname(__file__))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
FLASK_DEBUG = 1
SQLALCHEMY_DATABASE_URI = "sqlite:///db.drones.sqlite3"
