from app import db
from datetime import datetime

# create table user (
# 	uid int primary key autoincrement,
# 	openid varchar(50) not null,
# 	studentID varchar(11) not null,
# 	studentPWD varchar(50) not null
# )

# class User(db.model):
# 	"""创建用户类型"""
# 	uid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
# 	nickname = db.Column(db.String(50), nullable=False)
# 	openid = db.Column(db.String(50), nullable=False)
# 	studentID = db.Column(db.String(11), nullable=False)
# 	studentPWD = db.Column(db.String(50), nullable=False)
# 	bindingTime = db.Column(db.Date, default=datetime.now, nullable=False)
# 	leftTime = db.Column(db.Date, default=datetime.now, nullable=False)
# 	__table__ = 'hbu_user'


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(50), unique=True, nullable=False)
    studentID = db.Column(db.String(11), nullable=False)
    studentPWD = db.Column(db.String(50), nullable=False)
    bindingTime = db.Column(db.Date, default=datetime.now, nullable=False)
    leftTime = db.Column(db.Date, default=datetime.now, nullable=False)


class Material(db.Model):
    """关键字回复素材模型"""
    __tablename__ = 'materials'
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mtype = db.Column(db.String(10), nullable=False)
    keyword = db.Column(db.String(20), unique=True, nullable=False)
    content = db.Column(db.Text)
    media_id = db.Column(db.String(50))
    title = db.Column(db.String(60))
    description = db.Column(db.String(100))
    music_url = db.Column(db.String(2000))
    hqmusic_url = db.Column(db.String(2000))
    pic_url = db.Column(db.String(2000))
    url = db.Column(db.String(2000))
