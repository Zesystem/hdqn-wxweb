##########################################
#
# 扩展
# author: TuYaxuan
# time: 2019/3/14
# 说明: 防循环引用
#
###########################################

from multiprocessing import Lock
lock = Lock()

from app.utils.hbujwxt import HbuJwxt
hbujwxt = HbuJwxt()

from app.wxapi.message import MessageBuilder, MessageProcessor
mp = MessageProcessor(MessageBuilder())

def render(file, openid=True, **kwargs):
    from flask import render_template, request
    if openid :
        return render_template(file, openid=request.args.get('openid'), **kwargs)
    return render_template(file, **kwargs)