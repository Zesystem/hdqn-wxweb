from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
from app import models
db.create_all()

from app.utils.hbujwxt import HbuJwxt
hbujwxt = HbuJwxt()

from app import views















