###########################
#                         #
# weixin admin web        #
#                         #
###########################
from app.utils.fileutil import create_file
from flask import render_template, Blueprint, redirect

admin = Blueprint('admin', __name__)

user = {
	'name':'admin',
	'info':'超级管理员',
	'number':1
}

@admin.route('/index')
def index():
	return render_template('admin/index.html',user = user)

@admin.route('/login')
def login():
	return render_template('admin/login.html')

#查看反馈
@admin.route('/hxb')
def hxb():
	return render_template('admin/feedback/hxb.html',user = user)

@admin.route('/hxz')
def hxz():
	return render_template('admin/feedback/hxz.html',user = user)

@admin.route('/hzg')
def hzg():
	return render_template('admin/feedback/hzg.html',user = user)
#添加回复
@admin.route('/addTextAn')
def addTextAn():
	return render_template('admin/addanswer/addTextAnswear.html',user = user)

@admin.route('/addImageAn')
def addImageAn():
	return render_template('admin/addanswer/addImageAnswear.html',user = user)

@admin.route('/addImageContent')
def addImageContent():
	return render_template('admin/addanswer/addImageContent.html',user = user)

@admin.route('/addMusic')
def addMusic():
	return render_template('admin/addanswer/addMusic.html',user = user)
@admin.route('/addVideo')
def addVideo():
	return render_template('admin/addanswer/addVideo.html',user = user)

@admin.route('/addVoice')
def addVoice():
	return render_template('admin/addanswer/addVoice.html',user = user)
#回复管理
@admin.route('/lookImage')
def lookImage():
	return render_template('admin/answer/lookImage.html',user = user)

@admin.route('/lookText')
def lookText():
	return render_template('admin/answer/lookText.html',user = user)

@admin.route('/lookImageContent')
def lookImageContent():
	return render_template('admin/answer/lookImageContent.html',user = user)

@admin.route('/lookMusic')
def lookMusic():
	return render_template('admin/answer/lookMusic.html',user = user)

@admin.route('/lookVideo')
def lookVideo():
	return render_template('admin/answer/lookVideo.html',user = user)

@admin.route('/lookVoice')
def lookVoice():
	return render_template('admin/answer/lookVoice.html',user = user)

#数据管理
@admin.route('/jieKou')
def jieKou():
	return render_template('admin/statistics/jieKou.html',user = user)

@admin.route('/keyWord')
def keyWord():
	return render_template('admin/statistics/keyWords.html',user = user)

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
