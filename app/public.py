##########################################
#
# 公有路由 public
# author: TuYaxuan
# time: 2019/3/14
# 说明: 可以无需依赖验证登陆，快速链接使用的路由
#
###########################################


from app.exts import hbujwxt, render, lock
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

def render(file, openid=True, **kwargs):
    if openid :
        return render_template(file, openid=request.args.get('openid'), **kwargs)
    return render_template(file, **kwargs)

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
    return render('public/curriculum.html', timeinfo=timeinfo, curriculuminfo = curriculuminfo)

@public.route('/phone')
def phone():
    try:
        phones = [ {'address' : phone.address, 'phone' : phone.phone } for phone in PhoneList.query.all()]
    except:
        phones = []
    return render('/public/phone.html', phones=phones)

@public.route('/book')
def book():
    try:
        return render('/public/book.html', bookinfo=book_query(request.args.get('book_name')))
    except:
        return abort(404), 404

@public.route('/evaluate')
def evaluate():
    openid = request.args.get('openid')
    if not openid:
        return abort(404), 404
    curArr = []
    user = UserProcessor.get_user(openid)
    userinfo = {'username':user.studentID, 'password':user.studentPWD}
    lock.acquire()
    courseinfo = hbujwxt.evaluation_get_courses(userinfo)
    lock.release()
    if request.method == 'GET':
        if not request.args.get('premsg'):
            return render('/wxweb/Evaluate/index.html', courseinfo=courseinfo)
        else:
            try:
                course = courseinfo['data']['course'][int(request.args.get('premsg'))]
                courseinfo = hbujwxt.evaluation_get_detail(course[-1])
            except:
                courseinfo = {'code' : code.CODE_FAILED}
            if courseinfo['code'] == status.CODE_SUCCESS:
                courseinfo['data']['course'] = course
            return render('/wxweb/Evaluate/detail.html', courseinfo=courseinfo)
    else:
        try:
            course = courseinfo['data']['course'][int(request.args.get('premsg'))]
            courseinfo = hbujwxt.evaluation_get_detail(course[-1])
            data = request.form.to_dict()
            if data == {}:
                return "<script>alert('请填写完整数据！');window.history.back();</script>"
            else:
                for key in data:
                    if data[key] is None:
                        return "<script>alert('请填写完整数据！');window.history.back();</script>"
                res = hbujwxt.evaluation_post(data)
                if res['code'] == status.CODE_SUCCESS:
                    return "<script>alert('评教成功！');window.history.back();</script>"
                else:
                    return "<script>alert('评教失败！');window.history.back();</script>"
        except:
            return "<script>alert('非法提交！');window.location.href='/wxweb/index?openid=%s';</script>"%openid

@public.route('/spareclassroom', methods=['GET', 'POST'])
def spareclassroom():
    if request.method == 'GET':
        return render('public/spareclassroom.html', spareinfo=spare_params())
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