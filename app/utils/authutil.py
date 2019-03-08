import requests

APPID = 'wxc0eb1bc035f33f2e'
APPSECRET = 'e7d864d5a694045387bad0b77321b17b'

# APPID = 'wxc26075c6f39886a3'
# APPSECRET = 'c135f9a637faf20aebf705b7f6ce43f6'

def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'.format(
        appid = APPID,
        appsecret = APPSECRET
    )
    res = requests.request('GET', url).json()
    if res.get('errocode') is not None:
        return {'code': 404}
    else:
        return {'code': 200, 'access_token' : res['access_token']}

def batch_get(self, access_token, media_type, offset=0, count=20):
    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={access_token}".format(access_token=access_token)
    data = {
        'type' : media_type,
        'offset' : offset,
        'count' : count
    }
    res = requests.request('POST', url, data=data).json()
    print(res)

if __name__ == '__main__':
   # print(get_access_token()['access_token'])
   batch_get(get_access_token()['access_token'], 'news', 0, 20)