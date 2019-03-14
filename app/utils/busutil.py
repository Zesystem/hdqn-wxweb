##########################################
#
# 公交查询工具函数封装
# author: TuYaxuan
# time: 2019/3/14
#
###########################################


import requests
from app.utils import status

APPKEY = '503baf038567ce10' #公交查询api-appkey

def nearbystation_query(address, city='保定'):
    try:
        if address.isspace():
            return {'code' : status.CODE_EMPTY}
        url = 'http://api.jisuapi.com/transit/nearby?city={city}&address={address}&appkey={appkey}'.format(
            city = city,
            address = address,
            appkey = APPKEY
        )
        resp = requests.post(url).json() # get(url).json()
        if resp['status'] == '0':
            res = []
            for item in resp['result']:
                res.append(item['station'])
            return {'code' : status.CODE_SUCCESS, 'data' : res}
        return {'code' : status.CODE_NOT_EXIST}
    except:
        return {'code' : status.CODE_UNKNOW}

def line_query(lineno, city='保定'):
    try:
        if type(lineno) == int:
            lineno = str(lineno)
        if lineno.isspace():
            return {'code' : status.CODE_EMPTY}
        url = 'http://api.jisuapi.com/transit/line?city={city}&transitno={lineno}&appkey={appkey}'.format(
            city = city,
            lineno = lineno,
            appkey = APPKEY
        )
        resp = requests.post(url).json() # get(url).json()
        if resp['status'] == '0':
            if len(resp['result']) > 0:
                items = resp['result'][0].get('list',[])
            res = [ item['station'] for item in items]
            return {'code' : status.CODE_SUCCESS, 'data' : res}
        return {'code' : status.CODE_NOT_EXIST}
    except:
        return {'code' : status.CODE_UNKNOW}

def transfer_query(start, end, city='保定'):
    try:
        if start.isspace() or end.isspace():
            return {'code' : status.CODE_EMPTY}
        url = 'http://api.jisuapi.com/transit/station2s?city={city}&start={start}&end={end}&appkey={appkey}'.format(
            appkey = APPKEY,
            city = city,
            start = start,
            end =  end
        )
        resp = requests.post(url).json() # get(url).json()
        if resp['status'] == '0':
            res, items = [], []
            if len(resp['result']) > 0:
                items = resp['result'][0].get('steps', [])
            for item in items:
                res.append(item['steptext'])
            return {'code' : status.CODE_SUCCESS, 'data' : res}
        return {'code' : status.CODE_NOT_EXIST}
    except:
        return {'code' : status.CODE_UNKNOW}

if __name__ == '__main__':
    #print(nearbystation_query('河北大学'))
    #print(line_query('27'))
    print(transfer_query('河北大学北院', '火车站西广场'))
