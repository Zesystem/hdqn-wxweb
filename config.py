##########################################
#
# 应用配置
# author: TuYaxuan
# time: 2019/3/14
# 说明: 多环境配置将用于整个app应用
#
###########################################

import os, redis

class Config:
    CSRF_ENABLED = True
    SESSION_USE_SIGNER = True
    # PERMANENT_SESSION_LIFETIME = 3600
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ae03e9376259cbb9aec32cf4e1c96489d76129f1f6440f3d'

    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'app_wechat:' 
    SESSION_REDIS = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)

    #WXWEB_REDIS = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)

    # CACHE_TYPE = 'redis'
    # CACHE_REDIS_HOST = '127.0.0.1'
    # CACHE_REDIS_PORT = 6379
    # CACHE_REDIS_DB =  ''
    # CACHE_REDIS_PASSWORD = ''

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/upload')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp3', 'mp4', 'amr', 'JPG', 'PNG', 'JPEG', 'MP3', 'MP4', 'AMR'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    APP_DOMAIN = 'http://newtorn.fastfuck.me/'
    APPID = 'wxc26075c6f39886a3'
    APPSECRET = 'c135f9a637faf20aebf705b7f6ce43f6'

    SQLALCHEMY_DATABASE_URI  = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        'mysql',
        'mysqlconnector',
        'root',
        '199892.lw',
        '127.0.0.1',
        '3306',
        'app_wechat'
    )


class TestingConfig(Config):
    TESTING = False
    APP_DOMAIN = 'http://newtorn.fastfuck.me/'
    APPID = 'wxc26075c6f39886a3'
    APPSECRET = 'c135f9a637faf20aebf705b7f6ce43f6'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        'mysql',
        'mysqlconnector',
        'root',
        '199892.lw',
        '127.0.0.1',
        '3306',
        'app_wechat'
    )


class ProductionConfig(Config):
    DEBUG = False
    APP_DOMAIN = 'http://twwx.hbu.edu.cn/'
    APPID = 'wx4f8c3ea1b0707296'
    APPSECRET = '9dc17aaa34b373d748724a114fdac01d'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        'mysql',
        'mysqlconnector',
        'root',
        '',
        '127.0.0.1',
        '3306',
        'app_wechat'
    )


config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'default' : DevelopmentConfig
}
