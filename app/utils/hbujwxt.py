##########################################
#
# 教务系统工具类封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: 依赖bs4解析,pytesseract验证码识别
#
###########################################


import io
import os
import PIL
import random
import urllib
import requests
import pytesseract
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from app.utils import status

class HbuJwxt(object):
    '''
    河北大学综合教务系统
    '''
    def init(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.ip = '202.206.1.160'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Connection' : 'keep-alive',
            'Upgrade-Insecure-Requests': '1',  # important data
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control' : 'max-age=0',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Host' : self.ip,
            'Origin' : 'http://' + self.ip
        }

    def jw_login(self, userinfo, until=True):
        '''
        登陆教务系统
        '''
        def get_captcha():
            # 教务系统登陆验证码获取
            url = 'http://{ip}/validateCodeAction.do?random={rd}'.format(ip=self.ip, rd=random.random())
            res = self.session.request('GET', url, headers=self.headers)
            # string--》bytes--》stream
            data_stream = io.BytesIO(res.content)
            im = PIL.Image.open(data_stream)

            # 验证码识别
            im = im.convert('L')  # 灰度

            def initTable(threshold=140):
                table = []
                for j in range(256):
                    if j < threshold:
                        table.append(0)
                    else:
                        table.append(1)
                return table
            im = im.point(initTable(), '1')
            im = im.resize((400, 160))  # 拉伸
            code = pytesseract.image_to_string(im)  # 识别
            code = code.replace(' ', '')
            return code

        def login(captcha):
            '''
            教务系统登陆接口
            '''
            url = 'http://{ip}/loginAction.do'.format(ip = self.ip)
            self.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
            })
            data = {
                'zjh1': '',
                'tips': '',
                'lx': '',
                'evalue': '',
                'eflag': '',
                'fs': '',
                'dzslh': '',
                'zjh': userinfo['username'],
                'mm': userinfo['password'],
                'v_yzm': captcha
            }
            data = urllib.parse.urlencode(data, encoding='GBK')  # 需要from-urlencode
            res = self.session.request('POST', url, headers=self.headers, data=data)
            return res.content.decode('GBK', 'ignore')
        self.init()
        self.headers['Referer'] = 'http://{ip}/'.format(ip=self.ip)
        cnt = 0
        while cnt < 6:
            captcha = get_captcha()
            retcode = login(captcha)
            if '学分制综合教务' in retcode:
                # print('[+]Succes to login zhjw')
                return True
            if not until:
                cnt += 1
        # print('[-]Failed to login zhjw')
        return False

    def query_schoolrool(self, userinfo = None):
        '''
        查询学籍
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=1'.format(ip=self.ip)
            url = 'http://{ip}/xjInfoAction.do?oper=xjxx'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            baseinfo = {
                '学号': '',
                '姓名': '',
                '性别': '',
                '学生类别': '',
                '学籍状态': '',
                '是否有学籍': '',
                '身份证号': '',
                '考区': '',
                '高考考生号': '',
                '校区': '',
                '系所': '',
                '专业': '',
                '班级': '',
                '年级': '',
                '入学日期': '',
                '培养方式': '',
                '培养层次': ''
            }
            soup = BeautifulSoup(res.content.decode('GBK', 'ignore'), 'lxml')
            infotbl = soup.find("table", class_="titleTop3")
            infotds = infotbl.find_all("td")
            infotds.pop(0)
            for infokey in baseinfo.keys():
                for infotd in infotds:
                    if infotd.text.strip().startswith(infokey):
                        baseinfo[infokey] = infotds[infotds.index(infotd) + 1].text.strip()
                        break
            return {'code': status.CODE_SUCCESS, 'data': baseinfo}
        except:
            return {'code': status.CODE_FAILED}

    def query_this_term_score(self, userinfo = None):
        '''
        本学期成绩
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers.pop('Content-Type')
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=6'.format(ip=self.ip)
            url = 'http://{ip}/bxqcjcxAction.do'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.content.decode('GBK', 'ignore'), 'lxml')
            infotbl = soup.find("table", class_="displayTag")
            infotds = infotbl.find_all("td")
            scores = []
            count = int(len(infotds)/12)
            for cnt in range(count):
                base = cnt*12
                score = []
                for offset in range(12):
                    if offset in (2, 9, 10):
                        score.append(infotds[base+offset].text.strip())
                scores.append(score)
            return {'code': status.CODE_SUCCESS, 'data': scores}
        except:
            return {'code': status.CODE_FAILED}

    def query_each_term_score(self, userinfo=None):
        '''
        所有成绩
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers.pop('Content-Type')
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=6'.format(ip=self.ip)
            url = 'http://{ip}/gradeLnAllAction.do?type=ln&oper=qb'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.content.decode('GBK'), 'lxml')
            iframe = soup.find("iframe")
            url = 'http://{ip}/'.format(ip=self.ip) + iframe.get('src')
            self.headers['Referer'] = 'http://{ip}/gradeLnAllAction.do?type=ln&oper=qb'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.content.decode('GBK', 'ignore'), 'lxml')
            term_names = []
            terms = soup.find_all('a')
            for term in terms:
                term_names.append(term.get('name').strip())
            infotbls = soup.find_all('table', 'titleTop2')
            grade = 1
            name_idx = 0
            all_scores = []
            for infotbl in infotbls:
                scoretbl = infotbl.find('table', id='user')
                scoretds = scoretbl.find_all('td')
                scores = []
                count = int(len(scoretds)/7)
                for idx in range(count):
                    base = idx*7
                    score = []
                    for offset in range(7):
                        if offset in (2, 6):
                            score.append(scoretds[base+offset].text.strip())
                    scores.append(score)
                all_scores.append({'term_name': term_names[name_idx], 'scores': scores})
            return {'code': status.CODE_SUCCESS, 'data': all_scores}
        except:
            return {'code': status.CODE_FAILED}

    def query_course_table(self, userinfo=None):
        '''
        本学期课表
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=2'.format(ip=self.ip)
            url = 'http://{ip}/xkAction.do?actionType=6'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.content.decode('GBK', 'ignore'), 'lxml')
            infotds = soup.find('table', class_='displayTag').find_all('td')
            s, e = 9, 9+8*4
            swtds = infotds[s:e]
            s, e = e+2, e+2+8*4
            zwtds = infotds[s:e]
            s, e = e+2, e+2+8*4
            xwtds = infotds[s:e]
            infotds = swtds + zwtds + xwtds
            table = []
            for cnt in range(7):
                courses = []
                idx = cnt + 1
                while len(courses) < 11:
                    courses.append(infotds[idx].text.strip())
                    idx += 8
                table.append(courses)
            return {'code' : status.CODE_SUCCESS, 'data' : table}
        except:
            return {'code': status.CODE_FAILED}

    def evaluation_get_courses(self, userinfo=None):
        '''获取课程列表
        '''
        res = None
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=3'.format(ip=self.ip)
            url = 'http://{ip}/jxpgXsAction.do?oper=listWj'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            res = res.content.decode('GBK', 'ignore')
            soup = BeautifulSoup(res, features='lxml')
            table = soup.find('table', attrs={
                'class': "titleTop2",
                'width':"100%",
                'cellspacing':"0",
                'cellpadding':"0",
                'border':"0"
            })
            table = table.find('table', attrs={
                'class':"displayTag",
                'id':"user",
                'width':"100%",
                'cellspacing':"1",
                'cellpadding':"0",
                'border':"0"
            })
            head = []
            for th in table.thead.tr.find_all('th'):
                head.append(th.get_text().replace('\r\n', '').strip())
            courses = {
                'head' : head[0:-1],
                'course' : []
            }
            for tr in table.find_all('tr', recursive=False):
                item = []
                tds = tr.find_all('td', recursive=False)
                for td in tds[0:-1]:
                    item.append(td.get_text().replace('\r\n', '').strip())
                data = tds[-1].img.attrs.get('name').split('#@')
                item.append(
                    {
                        'wjbm':	data[0],
                        'bpr': data[1],
                        'pgnr': data[-1],
                        'oper': 'wjShow',
                        'wjmc': data[3],
                        'bprm': data[2],
                        'pgnrm': data[4],
                        'wjbz': '',
                        'pageSize': '20',
                        'page': '1',
                        'currentPage': '1',
                        'pageNo': ''
                    }
                )
                courses['course'].append(item)
            return {'code' : status.CODE_SUCCESS, 'data' : courses}
        except:
            return {'code': status.CODE_FAILED, 'res' : res}

    def evaluation_get_detail(self, data, userinfo = None):
        '''获取评教详情页
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers['Referer'] = 'http://{ip}/jxpgXsAction.do?oper=listWj'.format(ip=self.ip)
            data = urllib.parse.urlencode(data, encoding='GBK')
            url = 'http://{ip}/jxpgXsAction.do'.format(ip=self.ip)
            rep = self.session.request('POST', url, data, headers=self.headers)
            soup = BeautifulSoup(rep.content.decode('GBK'), features='lxml')
            table = soup.find('table',attrs={
                    'id':"tblView",
                    'cellspacing':"0",
                    'cellpadding':"0",
                    'border':"1"
            })

            content = {
                'selection' : [
                    ('(A)', '很满意', '10_1'),
                    ('(A)', '满意', '10_0.8'),
                    ('(A)', '基本满意', '10_0.6'),
                    ('(A)', '不满意', '10_0.2'),
                    ('(A)', '很不满意', '10_0'),
                ],
                'question' : []
            }

            for tr in table.find_all('tr', recursive=False):
                tds = tr.find_all('td', recursive=False)
                item = [tds[0].get_text().replace('\r\n', '').strip(), []]
                trs = tds[-1].table.find_all('tr')
                while len(trs) != 0:
                    question = trs.pop(0).td.get_text().replace('\r\n','').strip()
                    item[-1].append((question, trs.pop(0).td.input.attrs.get('name')))      
                content['question'].append(item)
            return {'code' : status.CODE_SUCCESS, 'data' : content}
        except:
            return {'code': status.CODE_FAILED}
    
    def evaluation_post(self, data, userinfo = None):
        '''教学评估提交
        '''
        try:
            if userinfo is not None and userinfo != {}:
                if not self.jw_login(userinfo):
                    return {'code': status.CODE_FAILED}
            self.headers['Referer'] = 'http://{ip}/jxpgXsAction.do'.format(ip=self.ip)
            data = urllib.parse.urlencode(data, encoding='GBK')
            url = 'http://{ip}/jxpgXsAction.do?oper=wjpg'.format(ip=self.ip)
            rep = self.session.request('POST', url, data, verify=False, headers=self.headers)
            # print(rep.text)
            if '评估成功' in rep.content.decode('GBK'):
                return {'code' : status.CODE_SUCCESS}
            return {'code' : status.CODE_FAILED}
        except:
            return {'code': status.CODE_FAILED}

if __name__ == '__main__':
    pass
    # hbujwxt = HbuJwxt()
    # userinfo = {'username':'20171004116', 'password':'20171004116'}
    # # print(hbujwxt.query_schoolrool(userinfo))
    # # print(hbujwxt.query_this_term_score(userinfo))
    # # print(hbujwxt.query_each_term_score(userinfo))
    # # print(hbujwxt.query_course_table(userinfo))
    # courses = hbujwxt.evaluation_get_courses(userinfo)
    # course = courses['data']['course'][3]
    # # print(courses)
    # detail = hbujwxt.evaluation_get_detail(course[-1])
    # print(detail)
    # data = {
    #     'wjbm': '0000000313',
    #     'bpr': '30736',
    #     'pgnr': 'Ty0022',
    #     'xumanyzg' : 'zg',
    #     'wjbz': '',
    #     '0000000008' : '10_1',
    #     '0000000010' : '10_1',
    #     '0000000016' : '10_1',
    #     '0000000017' : '10_1',
    #     '0000000018' : '10_1',
    #     '0000000019' : '10_1',
    #     '0000000020' : '10_1',
    #     '0000000024' : '10_1',
    #     '0000000025' : '10_1',
    #     '0000000026' : '10_1',
    #     'zgpj': '老师上课认真负责 同学们乐于听讲',
    # }
    # print(hbujwxt.evaluation_post(data))
    # print(hbujwxt.session.cookies)