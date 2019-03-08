###########################
#                         #
# weixin interface        #
#                         #
###########################
from app.wxapi import wxinter
from app.models import User
from app.exts import hbujwxt
from flask import render_template, Blueprint
from app.utils.formatutil import get_course_table
from app.utils.userprocess import UserProcessor
from app.utils.timeutil import week_now, month_now, day_after, get_week_day

inter = Blueprint('inter', __name__)

@inter.route('/')
def index():
    return render_template('public/wxinter.html')

@inter.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()

@inter.route('/curriculum/<openid>')
def curriculum(openid):
    curArr = []
    user = UserProcessor.get_user(openid)
    if user is not None:
        res = hbujwxt.query_course_table(userinfo = {'username':user.studentID, 'password':user.studentPWD})
        if res['code'] == 200:
            curArr = res['data']
    timeinfo = {'month' : month_now(), 'weekinfo' : get_week_day()}
    curriculuminfo = get_course_table(curArr)
    return render_template('public/curriculum.html', timeinfo=timeinfo, curriculuminfo = curriculuminfo)
