##########################################
#
# 公有路由 public
# author: TuYaxuan
# time: 2019/3/14
# 说明: 可以无需依赖验证登陆，快速链接使用的路由
#
###########################################


from app.exts import hbujwxt
from app.utils import status
from app.utils.bookutil import book_query
from app.utils.formatutil import get_course_table
from app.utils.userprocess import UserProcessor
from app.utils.spareclassroomutil import spare_params, spare_classroom
from flask import render_template, Blueprint, request, abort
from flask import session, url_for, jsonify
from app.models import User, PhoneList
from app.utils.timeutil import week_now, month_now, day_after, get_week_day

public = Blueprint('public', __name__)

@public.route('/curriculum')
def curriculum():
    openid = request.args.get('openid')
    if not openid:
        return abort(404), 404
    curArr = []
    user = UserProcessor.get_user(openid)
    if user is not None:
        res = hbujwxt.query_course_table(userinfo = {'username':user.studentID, 'password':user.studentPWD})
        if res['code'] == status.CODE_SUCCESS:
            curArr = res['data']
    timeinfo = {'month' : month_now(), 'weekinfo' : get_week_day()}
    curriculuminfo = get_course_table(curArr)
    return render_template('public/curriculum.html', timeinfo=timeinfo, curriculuminfo = curriculuminfo)

@public.route('/phone')
def phone():
    try:
        phones = [ {'address' : phone.address, 'phone' : phone.phone } for phone in PhoneList.query.all()]
    except:
        phones = []
    return render_template('/public/phone.html', phones=phones)

@public.route('/book')
def book():
    try:
        return render_template('/public/book.html', bookinfo=book_query(request.args.get('book_name')))
    except:
        return abort(404), 404

@public.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'GET':
        if request.args.get('openid'):
            session['openid'] = request.args.get('openid')
            if not User.query.filter(User.openid == session['openid']).first():
                return "<script>alert('此账户尚未绑定公众号！');window.history.back();</script>";
        elif not session.get('openid'):
            return render_template('wxweb/Error/index.html')
        if not request.args.get('premsg'):
            courses = [
                # {
                #     'tname' : '赵辰伟',
                #     'cname' : '团委自习课',
                #     'comment' : True
                # },
                # {
                #     'tname' : '谢博鋆',
                #     'cname' : '团委自习课',
                #     'comment' : False
                # }
            ]
            return render_template('/public/evaluate.html', courses=courses)
        else:
            course = {'tname' : '', 'cname' : ''}
            # course = {
            #     'tname' : '谢博鋆',
            #     'cname' : '团委自习课'
            # } 
            return render_template('/public/evaluate_detail.html', course=course)
    else:
        return "<script>alert('请填写完整数据！');window.history.back();</script>"

@public.route('/spareclassroom', methods=['GET', 'POST'])
def spareclassroom():
    if request.method == 'GET':
        return render_template('public/spareclassroom.html', spareinfo=spare_params())
    else:
        eduweek = request.form.get('eduweek')
        campus = request.form.get('campus')
        building = request.form.get('building')
        week = request.form.get('week')
        time = request.form.get('time')
        #print(eduweek, campus, building, week, time)
        if eduweek and campus and building and week and time:
            return jsonify(spare_classroom(eduweek, campus, building, week, time))
        else:
            return jsonify({'code' : status.CODE_FAILED})