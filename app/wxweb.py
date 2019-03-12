###########################
#                         #
# weixin micro web        #
#                         #
###########################
from flask import render_template, Blueprint, redirect
from flask import request, jsonify, session, url_for
from app import app_config
from app.exts import hbujwxt
from app.models import User, PhoneList
from app.wxapi import api
from app.utils import status
from app.utils.dbutil import text_query
from app.utils.bookutil import book_query
from app.utils.formatutil import get_course_table
from app.utils.timeutil import  month_now
from app.utils.weatherutil import getWeather
from app.utils.expressutil import express_query


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
    return  redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc26075c6f39886a3&{redirect_uri}&response_type=code&scope=snsapi_base&state=123#wechat_redirect'.format(
        redirect_uri = redirect_uri))

@wxweb.route('/code')
def code():
    wxcode = request.args.get('code')
    if not wxcode:
        return redirect(url_for('wxweb.home'))
    if not session.get('openid'):
        try:
            openid = api.get_token(wxcode).get('openid')
            session['openid'] = openid
        except:
            return redirect(url_for('wxweb.home'))
    return redirect(url_for('wxweb.index'))

@wxweb.route('/index')
def index():
    return render_template('/wxweb/index.html')
 
@wxweb.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        return render_template('/wxweb/Book/index.html')
    else:
        return jsonify(book_query(request.form.get('book_name')))

@wxweb.route('/bus')
def bus():
    return render_template('/wxweb/Bus/index.html')

@wxweb.route('/job')
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

@wxweb.route('/error')
def error():
	return render_template('/wxweb/Error/index.html')

@wxweb.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'GET':
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
            return render_template('/wxweb/Evaluate/index.html', courses=courses)
        else:
            course = {'tname' : '', 'cname' : ''}
            # course = {
            #     'tname' : '谢博鋆',
            #     'cname' : '团委自习课'
            # } 
            return render_template('/wxweb/Evaluate/detail.html', course=course)
    else:
        return "<script>alert('请填写完整数据！');window.history.back();</script>";


@wxweb.route('/family')
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
def feedback():
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
    try:
        phones = [ {'address' : phone.address, 'phone' : phone.phone } for phone in PhoneList.query.all()]
    except:
        phones = []
    return render_template('/wxweb/Phone/index.html', phones=phones)

@wxweb.route('/school')
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
def welfare():
    try:
        content = text_query('公益河大')
    except:
        content = ''
    return render_template('/wxweb/Welfare/index.html',content=content)

@wxweb.route('/score')
def score():
    try:
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


# data = [
#     ("研究生院办公室","5971132"),
#     ("文学院办公室","5079302"),
#     ("文学院团委","5079303"),
#     ("历史学院办公室","5077310"),
#     ("历史学院团委","5077302"),
#     ("新闻传播学院办公室","5079310"),
#     ("新闻传播学院团委","5079309"),
#     ("新闻学院团委","5079309"),
#     ("经济学院办公室","5079320"),
#     ("经济学院团委","5079327"),
#     ("管理学院办公室","5977048"),
#     ("管理学院团委","5079595"),
#     ("外国语学院办公室","5073256"),
#     ("外国语学院团委","5073257"),
#     ("教育学院办公室","5079334"),
#     ("教育学院团委","5079743"),
#     ("政法学院办公室","5079340"),
#     ("政法学院团委","5079339"),
#     ("艺术学院办公室","5073050"),
#     ("艺术学院团委","5073061"),
#     ("计算机科学与技术学院办公室","5079351"),
#     ("计算机科学与技术学院团委","5073087"),
#     ("数学与信息科学学院办公室","5079351"),
#     ("数学与信息科学学院团委","5079729"),
#     ("物理科学与技术学院办公室","5079354"),
#     ("物理科学与技术学院团委","5077315"),
#     ("化学与环境科学学院办公室","5079359"),
#     ("化学与环境科学学院团委","5079592"),
#     ("药学院办公室","5971107"),
#     ("药学院团委","5971107"),
#     ("生命科学学院办公室","5079364"),
#     ("生命科学学院团委","5079363"),
#     ("电子信息工程学院办公室","5079368"),
#     ("电子信息工程学院团委","5079367"),
#     ("建筑工程学院办公室","5079375"),
#     ("建筑工程学院团委","5079342"),
#     ("质量技术监督学院办公室","5092717"),
#     ("质量技术监督学院办公室","5079329"),
#     ("临床医学院办公室","5981697"),
#     ("护理学院办公室","5075665"),
#     ("护理学院团委","5075626"),
#     ("公共卫生学院办公室","5075639"),
#     ("公共卫生学院团委","5078509"),
#     ("基础医学院办公室","5079008"),
#     ("基础医学院团委","5097490"),
#     ("中医学院办公室","5075644"),
#     ("中医学院团委","5078514"),
#     ("继续教育学院办公室","5079378"),
#     ("人民武装学院办公室","0311-85200867"),
#     ("党委办公室","5079433"),
#     ("纪委办公室","5079650"),
#     ("党委组织部","5079438"),
#     ("党委宣传部","5079440"),
#     ("党委统战部","5079740"),
#     ("工会","5079466"),
#     ("校团委","5079462"),
#     ("校长办公室","5079709"),
#     ("人事处","5079468"),
#     ("老干部处","5079343"),
#     ("教务处","5079473"),
#     ("教师教学发展中心","5079371"),
#     ("学生处","5079444"),
#     ("心理健康","5977074"),
#     ("生活园区","5079410"),
#     ("就业办","5079445"),
#     ("国防教育","5971127"),
#     ("红色战线","5079693"),
#     ("国防生办","5077308"),
#     ("武装部","5079444"),
#     ("国有资产管理处办公室","5079507"),
#     ("保卫处","5079506"),
#     ("校园管理处","5079634"),
#     ("国际合作处","5079766"),
#     ("发展规划办公室","5079783"),
#     ("实验室管理办公室副主任室","5073999"),
#     ("学位委员会办公室副主任室","5977058"),
#     ("教育教学质量评估办公室副主任室","5977077"),
#     ("新校区管理与建设办公室","5073298"),
#     ("新闻中心","5079787"),
#     ("机关党委","5079576"),
#     ("网络中心","5079705"),
#     ("图书馆","5079425"),
#     ("档案馆","5071118"),
#     ("博物馆","5077063"),
#     ("期刊社","5079697"),
#     ("校友会","5079774"),
#     ("医学学科建设领导小组办公室","5079040"),
#     ("大学科技园管理办公室","5077331"),
#     ("河大社区","5079648"),
#     ("学术委员会","5079607"),
#     ("附属医院院办公室","5981680"),
#     ("校医院门诊","5079659"),
#     ("校医院南院医务","5079780"),
#     ("校医院新区医务","5929855"),
#     ("产业办公室","5079513"),
#     ("人工环境公司","5079567"),
#     ("出版社","5073003"),
#     ("赫达实业办公室","5079539"),
#     ("易百超市","5922099"),
#     ("赫达实业文印中心","5079546"),
#     ("赫达实业物业公司","5938587"),
#     ("赫达实业驾校","7532111"),
#     ("华萃园","5079694"),
#     ("主楼咖啡","5079564"),
#     ("新区咖啡","5073300"),
#     ("后勤综合部","7532000"),
#     ("后勤本部收发","5079714"),
#     ("后勤新区收发","5073088"),
#     ("后勤本部公寓","5079534"),
#     ("后勤新区公寓","5929920"),
#     ("餐饮公司办公室","5079559"),
#     ("医学部后勤服务公司办公室","5097499"),
#     ("高教学会办公室","5079759"),
#     ("关心下一代工作委员会办公室","5079436"),
#     ("关心老一辈工作委员会办公室","5079464"),
#     ("老教授协会办公室","5069575"),
#     ("马克思学院","5079448"),
#     ("外语教研部","5079405"),
#     ("数学教研部","5079658"),
#     ("体育教研部","5079409"),
#     ("计算中心办公室","5079390"),
#     ("文科综合实验教学中心办公室","5073888"),
#     ("医学实验中心办公室","5075522"),
#     ("宋史中心","5079415"),
#     ("医学部党支部","5079020"),
#     ("医学部行政办公室","5079021"),
#     ("医学部保卫科","5079034"),
#     ("工商学院团委","5073135"),
#     ("工商学院人文学部","6773055"),
#     ("工商学院经济管理学部","5073116"),
#     ("工商学院经济学部","5073116"),
#     ("工商学院信息科学与工程学部","6773077"),
#     ("工商学院信息学部","6773077"),
#     ("工商学院国际文化交流学部","6773066"),
#     ("附属医院","5981680"),
#     ("校医院","5079554"),
# ]

# from app import db
# from app.models import PhoneList
# @wxweb.route('/add_phone')
# def add_phone():
#     phones = []
#     for address, phone in data:
#         phones.append(PhoneList(
#             address = address,
#             phone = phone
#         ))
#     db.session.add_all(phones)
#     db.session.commit()
#     return 'Okay'