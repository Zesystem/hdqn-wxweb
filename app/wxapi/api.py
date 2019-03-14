##########################################
#
# 微信api工具函数封装
# author: TuYaxuan
# time: 2019/3/14
#
###########################################

import requests
from app import app_config

def get_web_auth_token(code):
    access_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={appsecret}&code={code}&grant_type=authorization_code'.format(
        appid = app_config.APPID,
        appsecret = app_config.APPSECRET,
        code = code
    )
    res = requests.get(access_url).json()
    return res