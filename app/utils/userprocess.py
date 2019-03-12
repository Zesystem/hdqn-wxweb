from flask import g
from app import db
from app.models import User
from app.utils import status
from app.utils.hbujwxt import HbuJwxt

class UserProcessor(object):
    @staticmethod
    def get_user(openid=None):
        openid = openid if openid is not None else g.get('openid')
        if openid is not None:
            return User.query.filter(User.openid == openid).first()
        return None

    @staticmethod
    def bind_user(user=None):
        user = user if user is not None else UserProcessor.get_user()
        if user is not None:
        	return status.CODE_EXIST
        elif HbuJwxt().jw_login(g.userinfo, until=False):
            db.session.add(User(openid = g.openid, 
            	studentID = g.userinfo['username'], 
            	studentPWD = g.userinfo['password']))
            db.session.commit()
            return status.CODE_SUCCESS
        return status.CODE_FAILED
    
    @staticmethod
    def unbind_user(user=None):
        user = user if user is not None else UserProcessor.get_user()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return status.CODE_SUCCESS
        return status.CODE_NOT_EXIST

    @staticmethod
    def update_user(user=None):
        user = user if user is not None else UserProcessor.get_user()
        if user is not None:
            if HbuJwxt().jw_login(g.userinfo, until=False):
                user.password = g.userinfo['password']
                db.session.commit()
                return status.CODE_SUCCESS
            else:
                return status.CODE_FAILED
        return status.CODE_NOT_EXIST


