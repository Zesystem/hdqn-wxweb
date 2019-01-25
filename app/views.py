from flask import render_template
from app import app
from app.wxapi import wxinter

###########################
#                         #
# weixin interface        #
#                         #
###########################

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()

@app.route('/')
@app.route('/wxweb/index')
def index():
	return render_template('wxinter.html')


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


