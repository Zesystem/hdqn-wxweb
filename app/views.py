from flask import render_template, url_for
from app import app
from app import db
from app.exts import hbujwxt

###########################
#                         #
# weixin interface        #
#                         #
###########################
from app.wxapi import wxinter
from app.models import User
from app.utils.formatutil import get_course_table
from app.utils.timeutil import week_now, month_now, day_after, get_week_day
from app.utils.userprocess import UserProcessor


@app.route('/wx', methods=['GET', 'POST'])
def wx():
    """微信token接口验证"""
    return wxinter.wx_check()

@app.route('/curriculum/<openid>')
def curriculum(openid):
    curArr = []
    user = UserProcessor.get_user(openid)
    if user is not None:
        res = hbujwxt.query_course_table(userinfo = {'username':user.studentID, 'password':user.studentPWD})
        if res['code'] == 200:
            curArr = res['data']
    timeinfo = {'month' : month_now(), 'weekinfo' : get_week_day()}
    curriculuminfo = get_course_table(curArr)
    return render_template('microweb/curriculum.html', timeinfo=timeinfo, curriculuminfo = curriculuminfo)


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


# ###########################
# #                         #
# # weixin admin web        #
# #                         #
# ###########################

# @app.route('/admin')
# def admin_index():
#     return render_template('wxinter.html')

# @app.route('/admin/login')
# def admin_login():
#     return '<div>admin login here!</div>'





# curArr = [
#     [
#         "",
#         "",
#         "",
#         "",
#         "大学体育4_18(本部虚拟教学楼场地10)",
#         "大学体育4_18(本部虚拟教学楼场地10)",
#         "",
#         "",
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#     ],
#     [
#         "数字逻辑与计算机组成实验_02(新校区C1座229)",
#         "数字逻辑与计算机组成实验_02(新校区C1座229)",
#         "数字逻辑与计算机组成实验_02(新校区C1座229)",
#         "",
#         "大学英语4_17(本部竞学楼（一教）313)",
#         "大学英语4_17(本部竞学楼（一教）313)",
#         "算法分析与设计实验_02(本部主楼403)",
#         "算法分析与设计实验_02(本部主楼403)",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)",
#     ],
#     [
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#         "数字逻辑与计算机组成_02(本部文林楼（九教）210)",
#         "",
#         "学生职业生涯规划_14(本部综合教学楼411)",
#         "学生职业生涯规划_14(本部综合教学楼411)",
#         "学生职业生涯规划_14(本部综合教学楼411)",
#         "",
#         "",
#         "",
#         "",
#     ],
#     [
#         "大学英语4_17(本部竞学楼（一教）416)",
#         "大学英语4_17(本部竞学楼（一教）416)",
#         "算法分析与设计_02(本部文林楼（九教）214)",
#         "算法分析与设计_02(本部文林楼（九教）214)",
#         "",
#         "",
#         "",
#         "",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)",
#         "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)",
#     ],
#     [
#         "",
#         "",
#         "",
#         "",
#         "汇编语言程序设计_02(本部综合教学楼106)",
#         "汇编语言程序设计_02(本部综合教学楼106)",
#         "汇编语言程序设计_02(本部综合教学楼106)",
#         "",
#         "算法分析与设计实验_02(本部主楼403)",
#         "算法分析与设计实验_02(本部主楼403)",
#         "",  
#     ],
#     [
#         "",
#         "",
#         "汇编语言程序设计实验_02(本部主楼403)",
#         "汇编语言程序设计实验_02(本部主楼403)",
#         "思想政治课社会实践_21(本部综合教学楼412)",
#         "思想政治课社会实践_21(本部综合教学楼412)",
#         "思想政治课社会实践_21(本部综合教学楼412)",
#         "思想政治课社会实践_21(本部综合教学楼412)",
#         "",
#         "",
#         "",
#     ],
#     [
#         "算法分析与设计_02(本部文林楼（九教）214)",
#         "算法分析与设计_02(本部文林楼（九教）214)",
#         "C#程序设计_02(本部文林楼（九教）128)",
#         "C#程序设计_02(本部文林楼（九教）128)",
#         "慢性病自我管理_01(本部综合教学楼501)",
#         "慢性病自我管理_01(本部综合教学楼501)",
#         "慢性病自我管理_01(本部综合教学楼501)",
#         "",
#         "C#程序设计实验_02(本部主楼403)",
#         "C#程序设计实验_02(本部主楼403)",
#         "",
#     ]
# ]





# array(7) {
#   [0]=>
#   array(11) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(0) ""
#     [3]=>
#     string(0) ""
#     [4]=>
#     string(47) "大学体育4_18(本部虚拟教学楼场地10)"
#     [5]=>
#     string(47) "大学体育4_18(本部虚拟教学楼场地10)"
#     [6]=>
#     string(0) ""
#     [7]=>
#     string(0) ""
#     [8]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [9]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [10]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#   }
#   [1]=>
#   array(11) {
#     [0]=>
#     string(58) "数字逻辑与计算机组成实验_02(新校区C1座229)"
#     [1]=>
#     string(58) "数字逻辑与计算机组成实验_02(新校区C1座229)"
#     [2]=>
#     string(58) "数字逻辑与计算机组成实验_02(新校区C1座229)"
#     [3]=>
#     string(0) ""
#     [4]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）313)"
#     [5]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）313)"
#     [6]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [7]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [8]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)"
#     [9]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)"
#     [10]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)"
#   }
#   [2]=>
#   array(11) {
#     [0]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [1]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [2]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [3]=>
#     string(0) ""
#     [4]=>
#     string(53) "学生职业生涯规划_14(本部综合教学楼411)"
#     [5]=>
#     string(53) "学生职业生涯规划_14(本部综合教学楼411)"
#     [6]=>
#     string(53) "学生职业生涯规划_14(本部综合教学楼411)"
#     [7]=>
#     string(0) ""
#     [8]=>
#     string(0) ""
#     [9]=>
#     string(0) ""
#     [10]=>
#     string(0) ""
#   }
#   [3]=>
#   array(11) {
#     [0]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）416)"
#     [1]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）416)"
#     [2]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [3]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [4]=>
#     string(0) ""
#     [5]=>
#     string(0) ""
#     [6]=>
#     string(0) ""
#     [7]=>
#     string(0) ""
#     [8]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)"
#     [9]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)"
#     [10]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)"
#   }
#   [4]=>
#   array(11) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(0) ""
#     [3]=>
#     string(0) ""
#     [4]=>
#     string(53) "汇编语言程序设计_02(本部综合教学楼106)"
#     [5]=>
#     string(53) "汇编语言程序设计_02(本部综合教学楼106)"
#     [6]=>
#     string(53) "汇编语言程序设计_02(本部综合教学楼106)"
#     [7]=>
#     string(0) ""
#     [8]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [9]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [10]=>
#     string(0) ""
#   }
#   [5]=>
#   array(11) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(50) "汇编语言程序设计实验_02(本部主楼403)"
#     [3]=>
#     string(50) "汇编语言程序设计实验_02(本部主楼403)"
#     [4]=>
#     string(56) "思想政治课社会实践_21(本部综合教学楼412)"
#     [5]=>
#     string(56) "思想政治课社会实践_21(本部综合教学楼412)"
#     [6]=>
#     string(56) "思想政治课社会实践_21(本部综合教学楼412)"
#     [7]=>
#     string(56) "思想政治课社会实践_21(本部综合教学楼412)"
#     [8]=>
#     string(0) ""
#     [9]=>
#     string(0) ""
#     [10]=>
#     string(0) ""
#   }
#   [6]=>
#   array(11) {
#     [0]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [1]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [2]=>
#     string(49) "C#程序设计_02(本部文林楼（九教）128)"
#     [3]=>
#     string(49) "C#程序设计_02(本部文林楼（九教）128)"
#     [4]=>
#     string(50) "慢性病自我管理_01(本部综合教学楼501)"
#     [5]=>
#     string(50) "慢性病自我管理_01(本部综合教学楼501)"
#     [6]=>
#     string(50) "慢性病自我管理_01(本部综合教学楼501)"
#     [7]=>
#     string(0) ""
#     [8]=>
#     string(40) "C#程序设计实验_02(本部主楼403)"
#     [9]=>
#     string(40) "C#程序设计实验_02(本部主楼403)"
#     [10]=>
#     string(0) ""
#   }
# }


# array(7) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(58) "数字逻辑与计算机组成实验_02(新校区C1座229)"
#     [2]=>
#     string(6) "FF4040"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [2]=>
#     string(6) "39E639"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）416)"
#     [2]=>
#     string(6) "FF9640"
#   }
#   [4]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [5]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [6]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [2]=>
#     string(6) "33CCCC"
#   }
# }
# array(3) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# array(7) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(58) "数字逻辑与计算机组成实验_02(新校区C1座229)"
#     [2]=>
#     string(6) "FFBF40"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [2]=>
#     string(6) "4671D5"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(56) "算法分析与设计_02(本部文林楼（九教）214)"
#     [2]=>
#     string(6) "FFDE40"
#   }
#   [4]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [5]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(50) "汇编语言程序设计实验_02(本部主楼403)"
#     [2]=>
#     string(6) "6A48D7"
#   }
#   [6]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(49) "C#程序设计_02(本部文林楼（九教）128)"
#     [2]=>
#     string(6) "9F3ED5"
#   }
# }
# array(4) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# array(7) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(47) "大学体育4_18(本部虚拟教学楼场地10)"
#     [2]=>
#     string(6) "B9F73E"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(48) "大学英语4_17(本部竞学楼（一教）313)"
#     [2]=>
#     string(6) "E6399B"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(53) "学生职业生涯规划_14(本部综合教学楼411)"
#     [2]=>
#     string(6) "FF4040"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [4]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(53) "汇编语言程序设计_02(本部综合教学楼106)"
#     [2]=>
#     string(6) "39E639"
#   }
#   [5]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='4'"
#     [1]=>
#     string(56) "思想政治课社会实践_21(本部综合教学楼412)"
#     [2]=>
#     string(6) "FF9640"
#   }
#   [6]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(50) "慢性病自我管理_01(本部综合教学楼501)"
#     [2]=>
#     string(6) "33CCCC"
#   }
# }
# array(1) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# array(3) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [2]=>
#     string(6) "FFBF40"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# array(5) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [4]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }

# array(7) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(65) "数字逻辑与计算机组成_02(本部文林楼（九教）210)"
#     [2]=>
#     string(6) "4671D5"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼107)"
#     [2]=>
#     string(6) "FFDE40"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='3'"
#     [1]=>
#     string(89) "毛泽东思想和中国特色社会主义理论体系概论_11(本部综合教学楼108)"
#     [2]=>
#     string(6) "6A48D7"
#   }
#   [4]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(47) "算法分析与设计实验_02(本部主楼403)"
#     [2]=>
#     string(6) "9F3ED5"
#   }
#   [5]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [6]=>
#   array(3) {
#     [0]=>
#     string(11) "rowspan='2'"
#     [1]=>
#     string(40) "C#程序设计实验_02(本部主楼403)"
#     [2]=>
#     string(6) "B9F73E"
#   }
# }
# array(2) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# array(4) {
#   [0]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [1]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [2]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
#   [3]=>
#   array(3) {
#     [0]=>
#     string(0) ""
#     [1]=>
#     string(0) ""
#     [2]=>
#     string(3) "fff"
#   }
# }
# ﻿








