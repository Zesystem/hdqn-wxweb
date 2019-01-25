import io
import os
import PIL
import random
import urllib
import requests
import pytesseract
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

class HbuJwxt(object):
    '''
    河北大学综合教务系统
    '''
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.ip = '202.206.1.160'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'  # important data
        }

    def jw_login(self, userinfo):
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
            data = urllib.parse.urlencode(data)  # 需要from-urlencode
            res = self.session.request(
                'POST', url, headers=self.headers, data=data)
            return res.text
        self.headers['Referer'] = 'http://{ip}/'.format(ip=self.ip)
        while True:
            captcha = get_captcha()
            retcode = login(captcha)
            if '学分制综合教务' in retcode:
                print('[+]Succes to login zhjw')
                return True
        print('[-]Failed to login zhjw')
        return False

    def query_schoolrool(self, userinfo):
        '''
        查询学籍
        '''
        try:
            if not self.jw_login(userinfo):
                return {'code': 404}
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
            soup = BeautifulSoup(res.text, 'lxml')
            infotbl = soup.find("table", class_="titleTop3")
            infotds = infotbl.find_all("td")
            for infokey in baseinfo.keys():
                for index in range(len(infotds)):
                    if infotds[index].text.strip().startswith(infokey):
                        baseinfo[infokey] = infotds[index + 1].text.strip()
                        break
            print(baseinfo)
            return {'code': 200, 'data': baseinfo}
        except:
            return {'code': 404}

    def query_this_term_score(self, userinfo):
        '''
        本学期成绩
        '''
        try:
            if not self.jw_login(userinfo):
                return {'code': 404}
            self.headers.pop('Content-Type')
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=6'.format(ip=self.ip)
            url = 'http://{ip}/bxqcjcxAction.do'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
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
            return {'code': 200, 'data': scores}
        except:
            return {'code': 404}

    def query_each_term_score(self, userinfo):
        '''
        所有成绩
        '''
        try:
            if not self.jw_login(userinfo):
                return {'code': 404}
            self.headers.pop('Content-Type')
            self.headers['Referer'] = 'http://{ip}/menu/menu.jsp?action1=0&index=6'.format(ip=self.ip)
            url = 'http://{ip}/gradeLnAllAction.do?type=ln&oper=qb'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
            iframe = soup.find("iframe")
            url = 'http://{ip}/'.format(ip=self.ip) + iframe.get('src')
            self.headers['Referer'] = 'http://{ip}/gradeLnAllAction.do?type=ln&oper=qb'.format(ip=self.ip)
            res = self.session.request('GET', url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
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
            return {'code': 200, 'data': all_scores}
        except:
            return {'code': 404}

if __name__ == '__main__':
    hbujwxt = HbuJwxt()
    userinfo = {'username':'20171004113', 'password':'199892.lw'}
    print(hbujwxt.query_schoolrool(userinfo))
    print(hbujwxt.query_this_term_score(userinfo))
    print(hbujwxt.query_each_term_score(userinfo))
