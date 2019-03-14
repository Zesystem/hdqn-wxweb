##########################################
#
# 微站后台管理路由 admin
# author: TuYaxuan
# time: 2019/3/14
# 说明: 管理应用素材
#
###########################################

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