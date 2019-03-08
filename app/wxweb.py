###########################
#                         #
# weixin micro web        #
#                         #
###########################
from flask import render_template, Blueprint, redirect

wxweb = Blueprint('wxweb', __name__)

user = {
	'name':'hhhhh',
	'key':1,
	'book':1,
	'month':10,
	'content':" ",
	'arr':['A','AB','B','BW','C','CD','D','DB','E'],
	'degree':["大一","大二","大三"],
	'score':["1","2","3","4"],
	'ch':["大一","大二","大三"]
}

@wxweb.route('/index')
def index():
	return render_template('/wxweb/index.html',user = user)

@wxweb.route('/book')
def book():
	return render_template('/wxweb/Book/index.html',user = user)

@wxweb.route('/bus')
def bus():
	return render_template('/wxweb/Bus/index.html',user = user)

@wxweb.route('/job')
def job():
	return render_template('/wxweb/CreateJob/index.html',user = user)

@wxweb.route('/error')
def error():
	return render_template('/wxweb/Error/index.html',user = user)

@wxweb.route('/evaluate')
def evaluate():
	return render_template('/wxweb/Evaluate/index.html',user = user)

@wxweb.route('/famliy')
def famliy():
	return render_template('/wxweb/Famliy/index.html',user = user)

@wxweb.route('/feedback')
def feedback():
	return render_template('/wxweb/Feedback/index.html',user = user)

@wxweb.route('/food')
def food():
	return render_template('/wxweb/Food/index.html',user = user)

@wxweb.route('/phone')
def phone():
	return render_template('/wxweb/Phone/index.html',user = user)

@wxweb.route('/school')
def school():
	return render_template('/wxweb/School/index.html',user = user)

@wxweb.route('/welfare')
def welfare():
	return render_template('/wxweb/Welfare/index.html',user = user)

@wxweb.route('/score')
def score():
	return render_template('/wxweb/Score/index.html',user=user)

@wxweb.route('/course')
def course():
	return render_template('/wxweb/Course/index.html',user=user)

@wxweb.route('/wether')
def wether():
	return render_template('/wxweb/Wether/index.html',user=user)

@wxweb.route('/express')
def express():
	return render_template('/wxweb/Express/index.html',user=user)	

@wxweb.route('/seat')
def seat():
	return render_template('/wxweb/Seat/index.html',user=user)

@wxweb.route('/foot')
def foot():
	return render_template('/wxweb/footnav.html',user=user);


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

# # @app.route('/wxweb/add_material')
# # def add_material():
# #     content = "欢迎关注河大青年！！！回复【菜单】获取帮助！！！"
# #     material = Material(mtype = 'text')
# #     db.session.add(material)
# #     db.session.commit()
# #     return  'Add successfully!'

# # @app.route('/wxweb/add_keyword')
# # def add_keyword():
# #     material = Material.query.filter(Material.mtype == 'image').first()
# #     if material is not None:
# #         keyword = KeyWord(word='菜单')
# #         keyword.material = material
# #         db.session.add(keyword)
# #         db.session.commit()
# #     return 'Add successfully!'


