##########################################
#
# 微站路由 wxweb
# author: TuYaxuan
# time: 2019/3/14
# 说明: 微站部分接口如成绩查询需要微信网页认证auth
#
###########################################


from flask import render_template, Blueprint, redirect
from flask import request, jsonify, session, url_for
from app import app_config, cache
from app.exts import hbujwxt
from app.models import User, PhoneList
from app.wxapi import api
from app.utils import status
from app.utils.dbutil import text_query
from app.utils.timeutil import  month_now
from app.utils.weatherutil import getWeather
from app.utils.expressutil import express_query
from app.utils.bookutil import book_query
from app.utils.formatutil import get_course_table
from app.utils.busutil import line_query, transfer_query, nearbystation_query

wxweb = Blueprint('wxweb', __name__)


@wxweb.context_processor
def user_context_processor():
    return {}

@wxweb.before_app_request
def user_before_request():
    if session.get('openid') and not session.get('user'):
        session['user'] = User.query.filter(User.openid == session['openid']).first()

@wxweb.route('/')
def home():
    import urllib.parse
    redirect_uri = urllib.parse.urlencode({'redirect_uri':'{app_domain}wxweb/code'.format(app_domain=app_config.APP_DOMAIN)})
    return  redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&{redirect_uri}&response_type=code&scope=snsapi_base&state=123#wechat_redirect'.format(
            appid = app_config.APPID,
            redirect_uri = redirect_uri))

@wxweb.route('/code')
def code():
    wxcode = request.args.get('code')
    if not wxcode:
        return redirect(url_for('wxweb.home'))
    if not session.get('openid'):
        try:
            print('hello')
            openid = api.get_web_auth_token(wxcode).get('openid')
            session['openid'] = openid
        except:
            return redirect(url_for('wxweb.home'))
    return redirect(url_for('wxweb.index'))

@wxweb.route('/index')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def index():
    return render_template('/wxweb/index.html')
 
@wxweb.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        return render_template('/wxweb/Book/index.html')
    else:
        return jsonify(book_query(request.form.get('book_name')))

@wxweb.route('/bus', methods=['GET', 'POST'])
def bus():
    if request.method == 'GET':
        return render_template('/wxweb/Bus/index.html')
    else:
        mt = request.form.get('mt')
        lineno = request.form.get('lineno')
        start, end = request.form.get('start'), request.form.get('end')
        if mt == 'l' and lineno:
            return jsonify(line_query(lineno))
        elif mt == 't' and start and end:
            return jsonify(transfer_query(start, end))
        else:
            return jsonify({'code' : status.CODE_FAILED})

@wxweb.route('/job')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def job():
    try:
        business = {
            'introduce' : text_query('创业基地简介'),
            'requirement' : text_query('入驻条件'),
            'process' : text_query('入驻程序'),
            'preferential' : text_query('创业优惠政策')
        }
    except:
         business = { 'introduce' : '', 'requirement' : '', 'process' : '', 'preferential' : ''}
    return render_template('/wxweb/CreateJob/index.html', business=business)

@wxweb.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'GET':
        if not session.get('openid'):
            return redirect(url_for('wxweb.home'))
        if not session.get('user'):
            return render_template('wxweb/Error/index.html')
        if not request.args.get('premsg'):
            courses = [
                # {
                #     'tname' : 'Admin',
                #     'cname' : 'Admin-Testing',
                #     'comment' : True
                # },
                # {
                #     'tname' : 'Developer',
                #     'cname' : 'Develop-Testing',
                #     'comment' : False
                # }
            ]
            return render_template('/wxweb/Evaluate/index.html', courses=courses)
        else:
            course = {'tname' : '', 'cname' : ''}
            # course = {
            #     'tname' : 'Developer',
            #     'cname' : 'Develop-Testing'
            # } 
            return render_template('/wxweb/Evaluate/detail.html', course=course)
    else:
        return "<script>alert('请填写完整数据！');window.history.back();</script>";


@wxweb.route('/family')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def family():
    try:
        info = {
            'apartment' : {
                'phone' : text_query('公寓电话'),
                'adjustment' : text_query('调宿服务'),
                'checkout' : text_query('退宿服务')
            },
            'international' : text_query('国交中心服务'),
            'logistics' : text_query('后勤报修')
        }
    except:
         info = { 'apartment' : { 'phone' : '', 'adjustment' : '', 'checkout' : ''}, 'international' : '', 'logistics' : ''}       
    return render_template('/wxweb/Family/index.html', info=info)

@wxweb.route('/feedback', methods=['GET', 'POST'])
@cache.cached(timeout=60*2, key_prefix='views_%s')
def feedback():
    return render_template('/wxweb/Feedback/index.html')

@wxweb.route('/food')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def food():
    schoolfood = {
        'specious' : '',
        'order' : '',
        'personal' : ''
    }
    return render_template('/wxweb/Food/index.html', schoolfood=schoolfood)

@wxweb.route('/phone')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def phone():
    try:
        phones = [ {'address' : phone.address, 'phone' : phone.phone } for phone in PhoneList.query.all()]
    except:
        phones = []
    return render_template('/wxweb/Phone/index.html', phones=phones)

@wxweb.route('/school')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def school():
    try:
        info = {
            'senses' : {
                'area' : ['本部', '新校区'], 
                'build' : [ 
                    ["主楼","熙园","易百超市"],
                    ['歌舞厅', '图书馆']
                ]
            },
            'wish' : text_query('洗衣服务'),
            'train' : text_query('培训信息'),
            'drive' : text_query('河大驾校'),
            'bookorder' : text_query('图书订购'),
            'yibaimarket' : text_query('易百超市')
        }
    except:
        info = {'senses' : {'area' : [], 'build' : [ [],['歌舞厅', '图书馆']] },'wish' : '','train' : '','drive' : '','bookorder' : '','yibaimarket' : ''}
    return render_template('/wxweb/School/index.html', info=info)

@wxweb.route('/welfare')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def welfare():
    try:
        content = text_query('公益河大')
    except:
        content = ''
    return render_template('/wxweb/Welfare/index.html',content=content)

@wxweb.route('/score')
def score():
    try:
        if not session.get('openid'):
            return redirect(url_for('wxweb.home'))
        if not session.get('user'):
            return render_template('wxweb/Error/index.html')
        grades = ['大一', '大二', '大三', '大四', '大五', '大六', '大七', '大八']
        resp = hbujwxt.query_each_term_score({'username': session['user'].studentID, 'password': session['user'].studentPWD})
        if resp['code'] == status.CODE_SUCCESS:
            resp = resp['data']
            user = {
                'grades' : grades[:int((len(resp)+1)/2)],
                'scores' : [term['scores'] for term in resp]
            }
    except:
        user = {'grades':[], 'scores':[]}
    return render_template('/wxweb/Score/index.html',user=user)

@wxweb.route('/course')
def course():
    try:
        if not session.get('openid'):
            return redirect(url_for('wxweb.home'))
        if not session.get('user'):
            return render_template('wxweb/Error/index.html')
        curArr = []
        res = hbujwxt.query_course_table(userinfo = {'username': session['user'].studentID, 'password': session['user'].studentPWD})
        if res['code'] == status.CODE_SUCCESS:
            curArr = res['data']
        courseinfo = {
            'month' : month_now(),
            'curriculuminfo' : get_course_table(curArr)
        }
    except:
        courseinfo = { 'month' : '', 'curriculuminfo' : ''}
    return render_template('/wxweb/Course/index.html',courseinfo=courseinfo)

@wxweb.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET':
        return render_template('/wxweb/Weather/index.html')
    else:
        return jsonify(getWeather(request.form.get('city_name')))

@wxweb.route('/express', methods=['GET', 'POST'])
def express():
    if request.method == 'GET':
        return render_template('/wxweb/Express/index.html')
    else:
        return jsonify(express_query(request.form.get('express_number')))

@wxweb.route('/seat')
@cache.cached(timeout=60*2, key_prefix='views_%s')
def seat():
    return render_template('/wxweb/Seat/index.html')
