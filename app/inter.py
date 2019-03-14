##########################################
#
# 微信后台验证路由 inter
# author: TuYaxuan
# time: 2019/3/14
# 说明: 用于公众号验证
#
###########################################

from app.wxapi import wxinter
from flask import render_template, Blueprint

inter = Blueprint('inter', __name__)

@inter.route('/')
def index():
    return render_template('public/wxinter.html')

@inter.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()