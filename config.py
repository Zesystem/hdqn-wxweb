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
DATABASE = 'app_hbuhelp'
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, MYSQL_HOST, MYSQL_PORT, DATABASE)

# SQLALCHEMY_DATABASE_URI = DB_URI

class Config:
    CSRF_ENABLED = True
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ae03e9376259cbb9aec32cf4e1c96489d76129f1f6440f3d'
    SQLALCHEMY_DATABASE_URI = DB_URI

    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'session:' 
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    DEBUG = False

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'default' : DevelopmentConfig
}