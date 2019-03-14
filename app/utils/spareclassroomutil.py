##########################################
#
# 空闲自习室工具函数封装
# author: TuYaxuan
# time: 2019/3/15
#
###########################################

import requests
from bs4 import BeautifulSoup
from app.utils import status

def spare_params():
    def get_option(sel_id):
        item_sel = soup.find(name='select', id=sel_id).find_all(name='option')
        item_now = ''
        items = []
        for item in item_sel:
            if item.get('selected') == 'selected':
                item_now = item.text
            items.append(item.text)
        return item_now, items
    try:
        url = 'http://yiban.hbu.cn/made_yiban/emptyClassroom/index.php'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')

        return {'code' : status.CODE_SUCCESS, 'data' : {
            'eduweek' : get_option('now'),
            'campus' : get_option('campus'),
            'building' : get_option('building'),
            'week' : get_option('week'),
            'time' : get_option('time')
        }}
    except:
        return {'code' : status.CODE_FAILED}

def spare_classroom(eduweek, campus, building, week, time):
    try:
        url = 'http://yiban.hbu.cn/made_yiban/emptyClassroom/result.php'
        data = {
            'now' : eduweek,
            'campus' : campus,
            'building' : building,
            'week' : week,
            'time' : time
        }
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 '\
                '(KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Referer' : 'http://yiban.hbu.cn/made_yiban/emptyClassroom/index.php',
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        resp = requests.post(url, data=data, headers=headers)
        if '未找到符合要求的空教室' in resp.text:
            return {'code' : status.CODE_NOT_EXIST}
        else:
            soup = BeautifulSoup(resp.text, 'lxml')
            res = soup.find(text='按条件筛选后，符合您的要求的空教室如下:').nextSibling.nextSibling
            return {'code' : status.CODE_SUCCESS, 'data' : res.strip().split('、')[:-1]}
    except:
        return {'code' : status.CODE_FAILED}


if __name__ == '__main__':
    print(spare_params())
    print(spare_classroom('3', '2', '一教', '4', '1'))