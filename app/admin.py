###########################
#                         #
# weixin admin web        #
#                         #
###########################
from flask import render_template, Blueprint, redirect, flash, url_for
from flask import session, request, abort, g
from app.utils.fileutil import create_file
from app.forms import LoginForm
from app.models import Admin, Role, Auth
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'account' not in session:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return decorated_function

def permission_control(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.rid == Admin.rid,
            Admin.account == session['account']
        ).first()
        all_auth = Auth.query.all()
        auths = admin.role.auths
        auths = list(map(lambda item: int(item), auths.split(',')))
        urls = [auth.url for auth in all_auth for admin_auth_id in auths if admin_auth_id == auth.auid]
        grp = request.url_rule.rule.split('/')
        rule = grp[2] if len(grp) > 2 else grp[1]
        if rule not in urls and admin.is_super != 0:
            abort(401)
        return func(*args, **kwargs)
    return decorated_function


@admin.context_processor
def admin_context_processor():
    return { 'user' : { 'name':session.get('account'), 'role':session.get('role')} }


@admin.route('/index')
@admin_login_req
@permission_control
def index():
	return render_template('admin/index.html')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('account') is not None:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter(Admin.account == data['account']).first()
        if not admin.check_password(data['password']):
            flash("Wrong password")
            return redirect(url_for('admin.login'))
        session['account'] = data['account']
        session['role'] = Role.query.filter(Role.rid == admin.rid).first().name
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@admin_login_req
def logout():
    session.pop('account', None)
    return redirect(url_for('admin.login'))

############################
# 查看反馈
############################

@admin.route('/LookFeedBack/hxb')
@admin_login_req
@permission_control
def hxb_feedback():
	return render_template('admin/feedback/hxb.html')

@admin.route('/LookFeedBack/hxz')
@admin_login_req
@permission_control
def hxz_feedback():
	return render_template('admin/feedback/hxz.html')

@admin.route('/LookFeedBack/hzg')
@admin_login_req
@permission_control
def hzg_feedback():
	return render_template('admin/feedback/hzg.html')

############################
# 添加回复
############################

@admin.route('/AddReply/textReply')
@admin_login_req
@permission_control
def text_reply():
	return render_template('admin/addreply/textReply.html')

@admin.route('/AddReply/imageReply')
@admin_login_req
@permission_control
def image_reply():
	return render_template('admin/addreply/imageReply.html')

@admin.route('/AddReply/newsReply')
@admin_login_req
@permission_control
def news_reply():
	return render_template('admin/addreply/newsReply.html')

@admin.route('/AddReply/musicReply')
@admin_login_req
@permission_control
def music_reply():
	return render_template('admin/addreply/musicReply.html')

@admin.route('/AddReply/videoReply')
@admin_login_req
@permission_control
def video_reply():
	return render_template('admin/addreply/videoReply.html')

@admin.route('/AddReply/voiceReply')
@admin_login_req
@permission_control
def voice_reply():
	return render_template('admin/addreply/voiceReply.html')

############################
# 回复管理
############################

@admin.route('/DelReply/index')
@admin_login_req
@permission_control
def del_index():
    return render_template('admin/base.html')

@admin.route('/ViewReply/ImageView')
@admin_login_req
@permission_control
def image_view():
	return render_template('admin/replymanage/imageView.html')

@admin.route('/ViewReply/textView')
@admin_login_req
@permission_control
def text_view():
	return render_template('admin/replymanage/TextView.html')

@admin.route('/ViewReply/newsView')
@admin_login_req
@permission_control
def news_view():
	return render_template('admin/replymanage/NewsView.html')

@admin.route('/ViewReply/musicView')
@admin_login_req
@permission_control
def music_view():
	return render_template('admin/replymanage/MusicView.html')

@admin.route('/ViewReply/videoView')
@admin_login_req
@permission_control
def video_view():
	return render_template('admin/replymanage/VideoView.html')

@admin.route('/ViewReply/voiceView')
@admin_login_req
@permission_control
def voice_view():
	return render_template('admin/replymanage/VoiceView.html')

############################
# 数据统计
############################

@admin.route('/DataCount/interfaceData')
@admin_login_req
@permission_control
def interface_data():
	return render_template('admin/datacount/interfaceData.html')

@admin.route('/DataCount/keyWordData')
@admin_login_req
@permission_control
def keyword_data():
	return render_template('admin/datacount/keywordData.html')

# @admin.route('/')
# def index():
#     return render_template('wxinter.html')

# @admin.route('/login')
# def login():
#     return '<div>admin login here!</div>'

# @admin.route('/addreply', methods=['POST'])
# def addreply():
#     res = request.form
#     if not res.get('type'):
#         return jsonify({'code' : 404})
#     if Material.query.filter(Material.keyword == res['keyword']).first() is not None:
#         return jsonify({'code' : 406})
#     material = Material(mtype=res['type'], keyword=res['keyword'])
#     right_post = True
#     if res['type'] in ('image', 'voice', 'video', 'music'):
#         file = request.files.get('filedata')
#         right_post &= file is not None
#         #rep = create_file(file)
#         material.media_id = 'media_id'
#     if res['type'] == 'text':
#         right_post &= res['content'].strip() != ""
#         material.content = res['content']
#     if res['type'] in ('video', 'music', 'news'):
#         right_post &= res['title'].strip() != "" and res['description'].strip() != ""
#         material.title = res['title']
#         material.description = res['description']
#     if res['type'] == 'music':
#         right_post &= res['music_url'].strip() != "" and res['hq_music_url'].strip() != ""
#         material.music_url = res['music_url']
#         material.hq_music_url = res['hq_music_url']
#     if res['type'] == 'news':
#         right_post &= res['pic_url'].strip() != "" and res['url'].strip() != ""
#         material.pic_url = res['pic_url']
#         material.url = res['url']
#     if not right_post:
#         return jsonify({'code' : 404})
#     db.session.add(material)
#     db.session.commit()
#     return jsonify({'code' : 200})

# {
#     'type' : 'text',
#     'keyword' : '你好',
#     'content' : '你好鸭!'
# }

# {
#     'type' : 'image',
#     'keyword' : '美女',
#     'filedata' : image_filedata
# }

# {
#     'type' : 'voice',
#     'keyword' : '心里话',
#     'filedata' : voice_filedata
# }

# {
#     'type' : 'video',
#     'keyword' : '校园宣传视频',
#     'title' : '河北大学宣传视频',
#     'description' : '河北大学宣传视频为你介绍河大的点点滴滴。',
#     'filedata' : video_filedata
# }

# {
#     'type' : 'music',
#     'keyword' : '天后',
#     'title' : '陈势安-天后',
#     'description' : '陈势安-天后，越听越动听。',
#     'filedata' : thumb_filedata,
#     'music_url' : '',
#     'hq_music_url' : ''
# }

# {
#     'type' : 'news',
#     'keyword' : '河大的点点滴滴',
#     'title' : '河大的点点滴滴',
#     'description' : '让我们感受河大的点点滴滴吧。'
#     'pic_url' : '',
#     'url' : ''
# }




########################################################################################

# from app import db
# from app.models import TextMaterial, NewsMaterial, VoiceMaterial, VideoMaterial, MusicMaterial, ImageMaterial


# @admin.route('/add_text')
# def add_text():
#     textmaterial = TextMaterial(
#         keyword = '我的学业',
#         content = '''好好学习，天天向上
# HELLO~我是河小博~发送：
# 【成绩查询】
# 【选课信息】
# 【我的课表】
# 【我的学籍】
# 【修改密码】
# 【绑定学号】
# 【解除绑定】
# 即可查询''')
#     db.session.add(textmaterial)
#     db.session.commit()
#     return 'Okay'


# @admin.route('/add_news')
# def add_news():
#     newsmaterial = NewsMaterial(
#         keyword = '河北大学',
#         title = '河大欢迎你',
#         description = '亲爱的新生，你们好，欢迎关注和大青年',
#         pic_url = 'http://www.hbu.edu.cn/u/cms/hbu/201711/07100234zsb9.jpg',
#         url  = 'http://www.hbu.edu.cn/'
#     )
#     db.session.add(newsmaterial)
#     db.session.commit()
#     return 'Okay'

# @admin.route('/add_voice')
# def add_voice():
#     voicematerial = VoiceMaterial(
#         keyword = '聆听河大',
#         media_id = 'thisisamediaid'
#     )
#     db.session.add(voicematerial)
#     db.session.commit()
#     return 'Okay'

# @admin.route('/add_video')
# def add_video():
#     videomaterial = VideoMaterial(
#         keyword = '看看河大',
#         media_id = 'thisisamediaid',
#         title = '看看河大',
#         description = '河大好风光～～河大真的大～～'
#     )
#     db.session.add(videomaterial)
#     db.session.commit()
#     return 'Okay'

# @admin.route('/add_music')
# def add_music():
#     musicmaterial = MusicMaterial(
#         keyword = '听听歌曲',
#         title = '动物世界-薛之谦',
#         description = '动物世界都太假',
#         music_url = 'https://m10.music.126.net/20190309191150/4c30c8a0f1d8fb8a567b27ac1ec169ea/ymusic/d444/4451/6e2c/665169e0e959fc602f8ed1315de4c13e.mp3',
#         hqmusic_url = 'https://m10.music.126.net/20190309191150/4c30c8a0f1d8fb8a567b27ac1ec169ea/ymusic/d444/4451/6e2c/665169e0e959fc602f8ed1315de4c13e.mp3'
#     )
#     db.session.add(musicmaterial)
#     db.session.commit()
#     return 'Okay'

# @admin.route('/add_image')
# def add_image():
#     imagematerial = ImageMaterial(
#         keyword = '河大图片',
#         media_id = 'thisisamedia'
#     )
#     db.session.add(imagematerial)
#     db.session.commit()
#     return 'Okay'

# from app import db
# @admin.route('/add_auth')
# def add_auth():
#     auths = []
#     auths.append(Auth(
#         name = '首页',
#         url = 'index'
#     ))
#     auths.append(Auth(
#         name = '查看反馈',
#         url = 'LookFeedBack'
#     ))
#     auths.append(Auth(
#         name = '添加回复',
#         url = 'AddReply'
#     ))
#     auths.append(Auth(
#         name = '删除回复',
#         url = 'DelReply'
#     ))
#     auths.append(Auth(
#         name = '查看回复',
#         url = 'ViewReply'
#     ))
#     auths.append(Auth(
#         name = '数据统计',
#         url = 'DataCount'
#     ))
#     for auth in auths:
#         db.session.add(auth)
#         db.session.commit()
#     return 'Okay'

# @admin.route('/add_role')
# def add_role():
#     roles = []
#     roles.append(Role(
#         name = '超级管理员',
#         auths = '1,2,3,4,5,6'
#     ))
#     roles.append(Role(
#         name = "普通管理员",
#         auths = '1,2,3,5,6'
#     ))
#     for role in roles:
#         db.session.add(role)
#         db.session.commit()
#     return 'Okay'

# @admin.route('/add_admin')
# def add_admin():
#     from werkzeug.security import generate_password_hash
#     admins = []
#     admins.append(Admin(
#         account = 'admin',
#         is_super = 0,
#         rid = 1,
#         password = generate_password_hash('hbutwwx,,,')
#     ))
#     admins.append(Admin(
#         account = 'newtorn',
#         is_super = 1,
#         rid = 2,
#         password = generate_password_hash('hbutwwx,,,')
#     ))
#     for admin in admins:
#         db.session.add(admin)
#         db.session.commit()
#     return 'Okay'