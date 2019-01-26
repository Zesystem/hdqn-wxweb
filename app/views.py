from flask import render_template
from app import app
from app import db

###########################
#                         #
# weixin interface        #
#                         #
###########################
from app.wxapi import wxinter
from app.models import User

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()

@app.route('/openid', methods=['GET', 'POST'])
def openid():
    return 'openid'

@app.route('/')
@app.route('/wxweb/index')
def index():
    return render_template('wxinter.html')

@app.route('/wxweb/bind_user')
def bind_user():
    openid = 'user_test_dev'
    studentID = '20171004113'
    studentPWD = '199892.lw'
    user = User.query.filter(User.openid == openid).first()
    if user is not None:
        return 'Bind failed! User has existed!'

    user = User(openid = openid, studentID = studentID, studentPWD = studentPWD)
    db.session.add(user)
    db.session.commit()
    return 'Bind successfully!'

@app.route('/wxweb/find_user')
def find_user():
    studentID = '20171004113'
    user = User.query.filter(User.studentID == studentID).first()
    if user is not None:
        print(user.studentID, user.studentPWD)
    return 'Find successfully!'

@app.route('/wxweb/update_user')
def update_user():
    studentID = '20171004113'
    user = User.query.filter(User.studentID == studentID).first()
    if user is not None:
        user.openid = 'update_user_test'
        db.session.commit()
    return 'Update successfully!'

@app.route('/wxweb/delete_user')
def delete_user():
    studentID = '20171004113'
    user = User.query.filter(User.studentID == studentID).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return 'Delete successfully!'

###########################
#                         #
# weixin micro web        #
#                         #
###########################

@app.route('/wxweb')
def wxweb_index():
    return render_template('wxinter.html')

@app.route('/wxweb/login')
def wxweb_login():
    return '<div>user login here!</div>'


###########################
#                         #
# weixin admin web        #
#                         #
###########################

@app.route('/admin')
def admin_index():
    return render_template('wxinter.html')

@app.route('/admin/login')
def admin_login():
    return '<div>admin login here!</div>'


###########################
#                         #
# weixin test html        #
#                         #
###########################

@app.route('/test')
def test():
    return render_template('test/test.html')


