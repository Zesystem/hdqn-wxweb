##########################################
#
# 图书查询工具函数封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: requests库请求、bs4解析
#
###########################################

import requests
import urllib.parse
from app.utils import status
from bs4 import BeautifulSoup

def book_query(book_name):
    if not book_name:
        return {'code': status.CODE_EMPTY}
    try:
        url = 'http://opac.hbu.edu.cn/opac_two/search2/searchout.jsp'
        data = {
            'search_no_type' : 'Y',
            'snumber_type' : 'Y',
            'suchen_type' : '1',
            'suchen_word' :  book_name,
            'suchen_match' : 'qx',
            'recordtype' : 'all',
            'library_id' : 'all',
            'show_type' : 'wenzi',
            'B1' : '确定',
        }
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://opac.hbu.edu.cn/opac_two/search2/search_simple.jsp?search_no_type=Y&snumber_type=Y&show_type=Z',
            'Upgrade-Insecure-Requests' : '1',
            'Host' : 'opac.hbu.edu.cn',
            'Origin': 'http://opac.hbu.edu.cn'
        }
        resp = requests.post(url, data=urllib.parse.urlencode(data, encoding='gbk'), headers=headers)
        soup = BeautifulSoup(resp.content.decode('gbk'), 'lxml')
        divwrap = soup.find('div', id='searchout_tuwen')
        infotrs = divwrap.find_all('tr')[1:]
        books = []
        for infotr in infotrs:
            infotds = infotr.find_all('td')
            total, borrowable = infotds[7].text.split('\xa0')[0:2]
            total, borrowable = total.split('：')[1], borrowable.split('：')[1]
            book = {
                'name' : infotds[1].text.strip(),
                'code' : infotds[6].text.strip(),
                'total' : total,
                'borrowable' : borrowable,
            }
            books.append(book)
        if books == []:
            return {'code': status.CODE_NOT_EXIST}
        return {'code': status.CODE_SUCCESS, 'data': books}
    except:
        return {'code': status.CODE_UNKNOW}

if __name__ == '__main__':
    books = book_query('朝花夕拾')
    print(books)