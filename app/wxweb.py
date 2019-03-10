###########################
#                         #
# weixin micro web        #
#                         #
###########################
from flask import render_template, Blueprint, redirect, g, abort
from app.exts import hbujwxt
from app.models import User, TextMaterial
from app.utils import status
from app.utils.userprocess import UserProcessor
from app.utils.formatutil import get_course_table
from app.utils.timeutil import week_now, month_now, day_after, get_week_day

wxweb = Blueprint('wxweb', __name__)

def text_query(key):
    text_material = TextMaterial.query.filter(TextMaterial.keyword == key).first()
    res = '' if text_material is None else text_material.content
    return "<br/>".join('<p>'+line+'</p>' for line in res.split('\n'))

@wxweb.context_processor
def user_context_processor():
    return {}

@wxweb.before_app_request
def user_before_request():
    if g.get('openid') is None:
        g.openid = 'oOBVv1cFS_mZnLps3GBhrMwQqac0'
        g.user = User.query.filter(User.openid == g.openid).first()

@wxweb.route('/index')
def index():
    return render_template('/wxweb/index.html')

@wxweb.route('/book')
def book():
    return render_template('/wxweb/Book/index.html')

@wxweb.route('/bus')
def bus():
    return render_template('/wxweb/Bus/index.html')

@wxweb.route('/job')
def job():
    business = {
        'introduce' : text_query('创业基地简介'),
        'requirement' : text_query('入驻条件'),
        'process' : text_query('入驻程序'),
        'preferential' : text_query('创业优惠政策')
    }
    print(business)
    return render_template('/wxweb/CreateJob/index.html', business=business)

@wxweb.route('/error')
def error():
	return render_template('/wxweb/Error/index.html')

@wxweb.route('/evaluate')
def evaluate():
    if g.get('user') is None:
        if g.get('openid') is not None:
            return render_template('/wxweb/Error/index.html')
    #     #return redirect('/wxweb/authorized')
    teacher = {
        'name' : '赵辰伟',
        'key' : 1
    }
    return render_template('/wxweb/Evaluate/index.html', teacher=teacher)

@wxweb.route('/famliy')
def famliy():
    apartment = {
        'phone' : '',
        'adjustment' : text_query('调宿服务'),
        'checkout' : text_query('退宿服务')
    }
    return render_template('/wxweb/Famliy/index.html', apartment=apartment)

@wxweb.route('/feedback')
def feedback():
    if g.get('user') is None:
        if g.get('openid') is not None:
            return render_template('/wxweb/Error/index.html')
    #     #return redirect('/wxweb/authorized')
    return render_template('/wxweb/Feedback/index.html')

@wxweb.route('/food')
def food():
    schoolfood = {
        'specious' : '',
        'order' : '',
        'personal' : ''
    }
    return render_template('/wxweb/Food/index.html', schoolfood=schoolfood)

@wxweb.route('/phone')
def phone():
    phones = ['A', 'B', 'C', 'D', 'E', 'F']
    return render_template('/wxweb/Phone/index.html', phones=phones)

@wxweb.route('/school')
def school():
    info = {
        'grades' : ["大一","大二","大三"],
        'wish' : '',
        'train' : '',
        'drive' : '',
        'bookorder' : '',
        'yibaimarket' : ''
    }
    return render_template('/wxweb/School/index.html', info=info)

@wxweb.route('/welfare')
def welfare():
    content = ''
    return render_template('/wxweb/Welfare/index.html',content=content)

@wxweb.route('/score')
def score():
    if g.get('user') is None:
        if g.get('openid') is not None:
            return render_template('/wxweb/Error/index.html')
    #     #return redirect('/wxweb/authorized')
    grades = ['大一', '大二', '大三', '大四', '大五', '大六', '大七', '大八']
    resp = hbujwxt.query_each_term_score({'username': g.user.studentID, 'password': g.user.studentPWD})
    if resp['code'] == status.CODE_SUCCESS:
        resp = resp['data']
        user = {
            'grades' : grades[:int((len(resp)+1)/2)],
            'scores' : [term['scores'] for term in resp]
        }
    return render_template('/wxweb/Score/index.html',user=user)

@wxweb.route('/course')
def course():
    if g.get('user') is None:
        if g.get('openid') is not None:
            return render_template('/wxweb/Error/index.html')
    #     #return redirect('/wxweb/authorized')
    curArr = []
    res = hbujwxt.query_course_table(userinfo = {'username': g.user.studentID, 'password': g.user.studentPWD})
    if res['code'] == status.CODE_SUCCESS:
        curArr = res['data']
    courseinfo = {
        'month' : month_now(),
        'curriculuminfo' : get_course_table(curArr)
    }
    return render_template('/wxweb/Course/index.html',courseinfo=courseinfo)

@wxweb.route('/wether')
def wether():
    return render_template('/wxweb/Wether/index.html')

@wxweb.route('/express')
def express():
    return render_template('/wxweb/Express/index.html')	

@wxweb.route('/seat')
def seat():
    return render_template('/wxweb/Seat/index.html')



# @app.route('/wxweb')
# def wxweb_index():
#     return render_template('wxinter.html')

# @app.route('/wxweb/login')
# def wxweb_login():
#     return '<div>user login here!</div>'

# @app.route('/')
# @app.route('/wxweb/index')
# def index():
#     return render_template('wxinter.html')

# @app.route('/wxweb/bind_user')
# def bind_user():
#     openid = 'user_test_dev'
#     studentID = '20171004113'
#     studentPWD = '199892.lw'
#     user = User.query.filter(User.openid == openid).first()
#     if user is not None:
#         return 'Bind failed! User has existed!'

#     user = User(openid = openid, studentID = studentID, studentPWD = studentPWD)
#     db.session.add(user)
#     db.session.commit()
#     return 'Bind successfully!'

# @app.route('/wxweb/find_user')
# def find_user():
#     studentID = '20171004113'
#     user = User.query.filter(User.studentID == studentID).first()
#     if user is not None:
#         print(user.studentID, user.studentPWD)
#     return 'Find successfully!'

# @app.route('/wxweb/update_user')
# def update_user():
#     studentID = '20171004113'
#     user = User.query.filter(User.studentID == studentID).first()
#     if user is not None:
#         user.openid = 'update_user_test'
#         db.session.commit()
#     return 'Update successfully!'

# @app.route('/wxweb/delete_user')
# def delete_user():
#     studentID = '20171004113'
#     user = User.query.filter(User.studentID == studentID).first()
#     if user is not None:
#         db.session.delete(user)
#         db.session.commit()
#     return 'Delete successfully!'

# @app.route('/wxweb/add_material')
# def add_material():
#     content = "欢迎关注河大青年！！！回复【菜单】获取帮助！！！"
#     material = Material(mtype = 'text')
#     db.session.add(material)
#     db.session.commit()
#     return  'Add successfully!'

# @app.route('/wxweb/add_keyword')
# def add_keyword():
#     material = Material.query.filter(Material.mtype == 'image').first()
#     if material is not None:
#         keyword = KeyWord(word='菜单')
#         keyword.material = material
#         db.session.add(keyword)
#         db.session.commit()
#     return 'Add successfully!'



# from app.wxapi.keywords import text_process
# from app.models import TextMaterial
# from app import db

# @wxweb.route('/add_text_reply')
# def add_text_reply():
#     all_material = []
#     for k, v in text_process.items():
#         all_material.append(TextMaterial(
#             keyword = k,
#             content = v
#         ))
#     db.session.add_all(all_material)
#     db.session.commit()
#     return 'Okay'