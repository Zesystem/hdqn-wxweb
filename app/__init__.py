import os
from flask import Flask
from config import config

app_config = config[os.getenv('FLASK_CONFIG') or 'default']

app = Flask(__name__)
app.config.from_object(app_config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from app import models
db.create_all()

# from app.models import create_admin
# create_admin()

from app import views

from flask_session import Session
Session(app)













