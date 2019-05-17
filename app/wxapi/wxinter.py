##########################################
#
# 微信toekn接口验证
# author: TuYaxuan
# time: 2019/3/14
# 说明: 微信公众平台验证
#
###########################################

import time
import hashlib
from app.exts import mp
from flask import request, make_response, render_template

def wx_check():
    """微信token接口验证"""
    data = request.args
    if len(data) == 0:
        return render_template('public/wxinter.html')
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')
    token = 'dev4hdqn'

    grp = [token, timestamp, nonce]
    grp.sort()
    hashcode = hashlib.sha1(''.join(grp).encode('utf-8')).hexdigest()

    # print("handle/GET func: hashcode, signature:", hashcode, signature)
    if hashcode != signature:
        return render_template('public/wxinter.html')
    else:
        if request.method == 'GET':
            if not echostr:
                return render_template('public/wxinter.html')
            return make_response(echostr)
        elif request.method == 'POST':
            rec = request.stream.read()
            if not rec:
                return render_template('public/wxinter.html')
            rep = mp.check_reply(rec)
            return rep