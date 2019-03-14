##########################################
#
# 数据库模型
# author: TuYaxuan
# time: 2019/3/14
# 说明: 依赖于appg配置的SQLAlchemy配置的实例db
#
###########################################

from app import db
from datetime import datetime


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(50), unique=True, nullable=False)
    studentID = db.Column(db.String(11), nullable=False)
    studentPWD = db.Column(db.String(50), nullable=False)
    bindingTime = db.Column(db.Date, default=datetime.now, nullable=False)
    leftTime = db.Column(db.Date, default=datetime.now, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.openid


class PhoneList(db.Model):
    """电话模型"""
    __tablename__ = 'phones'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<PhoneList %r>' % self.address


class FeedBack(db.Model):
    """反馈模型"""
    __tablename__ = 'feedbacks'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    content = db.Column(db.Text, nullable=False)
    navtype = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<FeedBack %r>' % self.openid

class TextMaterial(db.Model):
    """回复文本素材模型"""
    __tablename__ = 'textmaterials'
    tmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<TextMaterial %r>' % self.tmid
        

class NewsMaterial(db.Model):
    """回复图文素材模型"""
    __tablename__ = 'newsmaterials'
    nmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    pic_url = db.Column(db.String(2000), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return '<NewsMaterial %r>' % self.nmid


class VoiceMaterial(db.Model):
    """回复语音素材模型"""
    __tablename__ = 'voicematerials'
    vomid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    media_id = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<VoiceMaterial %r>' % self.vomid


class VideoMaterial(db.Model):
    """回复视频素材模型"""
    __tablename__ = 'videomaterials'
    vimid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    media_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<VideoMaterial %r>' % self.vimid


class MusicMaterial(db.Model):
    """回复音乐素材模型"""
    __tablename__ = 'musicmaterials'
    mmid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    music_url = db.Column(db.String(2000), nullable=False)
    hqmusic_url = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return '<MusicMaterial %r>' % self.mmid



class ImageMaterial(db.Model):
    """回复图片素材模型"""
    __tablename__ = 'imagematerials'
    imid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    keyword = db.Column(db.String(50), unique=True, nullable=False)
    media_id = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<ImageMaterial %r>' % self.imid


class Auth(db.Model):
    """权限模型"""
    __tablename__ = 'auths'
    auid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Auth %r>' % self.name


class Role(db.Model):
    """"角色模型"""
    __tablename__ = "roles"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    auths = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class Admin(db.Model):
    """管理员模型"""
    __tablename__ = 'admins'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_super = db.Column(db.SmallInteger)
    rid = db.Column(db.Integer, db.ForeignKey('roles.rid'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('AdminLog', backref='admin')
    operatelogs = db.relationship('OperateLog', backref='operate')

    def __repr__(self):
        return '<Admin %r>' % self.account

    def check_password(self, input_password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, input_password)

class AdminLog(db.Model):
    """管理员日志模型"""
    __tablename__ = 'adminlogs'
    alid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column(db.Integer, db.ForeignKey('admins.aid'))
    ip =  db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<AdminLog %r>' % self.alid

class OperateLog(db.Model):
    """操作日志模型"""
    __tablename__ = "operatelogs"
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column(db.Integer, db.ForeignKey('admins.aid'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<OperateLog %r>' % self.oid

# def create_admin():
#     # 添加角色
#     role = Role(
#         name="超级管理员",
#         auths="",
#     )
#     db.session.add(role)
#     db.session.commit()

#     # 添加管理员
#     from werkzeug.security import generate_password_hash

#     admin = Admin(
#         account = 'admin',
#         password = generate_password_hash('hbutwwx,,,'),
#         is_super = 0,
#         rid = role.rid,
#     )
#     db.session.add(admin)
#     db.session.commit()