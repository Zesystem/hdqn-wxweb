###########################
#                         #
# weixin interface        #
#                         #
###########################
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