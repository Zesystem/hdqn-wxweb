import os, redis

# CSRF_ENABLED = True
# import binascii
# SECRET_KEY = binascii.hexlify(os.urandom(24)).decode()

DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = '199892.lw'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
DATABASE = 'app_wechat'
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, MYSQL_HOST, MYSQL_PORT, DATABASE)

# SQLALCHEMY_DATABASE_URI = DB_URI

class Config:
    CSRF_ENABLED = True
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ae03e9376259cbb9aec32cf4e1c96489d76129f1f6440f3d'
    SQLALCHEMY_DATABASE_URI = DB_URI

    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'app_wechat:' 
    SESSION_REDIS = redis.StrictRedis(host='127.0.0.1', port='6379')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    APP_DOMAIN = 'http://newtorn.fastfuck.me/'
    APPID = 'wxc26075c6f39886a3'
    APPSECRET = 'c135f9a637faf20aebf705b7f6ce43f6'

class ProductionConfig(Config):
    DEBUG = False
    APP_DOMAIN = 'http://twwx.hbu.edu.cn/'
    APPID = 'wxc0eb1bc035f33f2e'
    APPSECRET = 'e7d864d5a694045387bad0b77321b17b'

class TestingConfig(Config):
    DEBUG = False
    APP_DOMAIN = 'http://newtorn.fastfuck.me/'
    APPID = 'wxc26075c6f39886a3'
    APPSECRET = 'c135f9a637faf20aebf705b7f6ce43f6'

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'default' : DevelopmentConfig
}