##########################################
#
# 快递查询工具函数封装
# author: TuYaxuan
# time: 2019/3/14
# 说明: requests库请求
#
###########################################

import requests
from app.utils import status

def express_query(express_number):
    if not express_number:
        return {'code': status.CODE_EMPTY}
    try:
        url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={postid}'.format(
            postid = express_number
        )
        resp = requests.get(url).json()
        autos = resp['auto']
        if len(autos) == 0:
            return {'code': status.CODE_NOT_EXIST}
        for auto in autos:
            express_type = auto['comCode']
            url = 'http://www.kuaidi100.com/query?type={express_type}&postid={postid}&temp=0.5592852748522015&phone='.format(
                express_type = express_type,
                postid = express_number
            )
            resp = requests.get(url).json()
            if resp['status'] == '200':
                return {'code': status.CODE_SUCCESS, 'data': resp['data']}
        return {'code': status.CODE_NOT_EXIST}
    except:
        return {'code': status.CODE_UNKNOW}

if __name__ == '__main__':
    print(express_query('804766116799741067'))