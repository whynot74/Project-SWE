# filepath: /c:/Users/zeyad/OneDrive/Desktop/Software project front+back/Project-SWE/flask-server/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from . import models