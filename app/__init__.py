##########################################
#
# app初始化
# author: TuYaxuan
# time: 2019/3/14
# 说明: 创建并配置用于app应用的对象初始化
#
###########################################


import os
from flask import Flask
from config import config
from flask_caching import Cache
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app_config = config[os.getenv('FLASK_CONFIG') or 'default']

cache = Cache()
db = SQLAlchemy()
sess = Session()
app = Flask(__name__)
app.config.from_object(app_config)

# 推送程序上下文
app_ctx = app.app_context()
app_ctx.push()

db.init_app(app)
sess.init_app(app)
cache.init_app(app)

from app import views

from app import models
db.create_all()

# 关闭推送
app_ctx.pop()








