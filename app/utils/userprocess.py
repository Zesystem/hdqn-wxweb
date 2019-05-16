##########################################
#
# 微信用户处理工具类封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: 依赖于User模型
#
###########################################

from flask import g
from app import db
from app.models import User
from app.utils import status
from app.exts import hbujwxt

class UserProcessor(object):
    @staticmethod
    def get_user(openid):
        if openid is not None:
            return User.query.filter(User.openid == openid).first()
        return None

    @staticmethod
    def bind_user(openid, userinfo, user=None):
        user = user if user is not None else UserProcessor.get_user(openid)
        if user is not None:
        	return status.CODE_EXIST
        elif hbujwxt.jw_login(userinfo, until=False):
            db.session.add(User(openid = openid, 
            	studentID = userinfo['username'], 
            	studentPWD = userinfo['password']))
            db.session.commit()
            return status.CODE_SUCCESS
        return status.CODE_FAILED
    
    @staticmethod
    def unbind_user(openid, user=None):
        user = user if user is not None else UserProcessor.get_user(openid)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return status.CODE_SUCCESS
        return status.CODE_NOT_EXIST

    @staticmethod
    def update_user(openid, userinfo, user=None):
        user = user if user is not None else UserProcessor.get_user(openid)
        if user is not None:
            if hbujwxt.jw_login(userinfo, until=False):
                user.studentPWD = userinfo['password']
                db.session.commit()
                return status.CODE_SUCCESS
            else:
                return status.CODE_FAILED
            return status.CODE_SUCCESS
        return status.CODE_NOT_EXIST
