from app.utils.hbujwxt import HbuJwxt
hbujwxt = HbuJwxt()

from app.wxapi.message import MessageBuilder, MessageProcessor
mp = MessageProcessor(MessageBuilder())

from flask import redirect, session, url_for
from functools import wraps
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function
