import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# 定义配置基类
# class Config:
#     # 秘匙
#     SECRET_KEY = os.environ.get('SECRENT_KEY') or 'hdqn-developer'

# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:pzl123456@localhost/develop-database'

# class TestingConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:pzl123456@localhost/test-database'

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:pzl123456@localhost/product-database'

# config = {
#     'development' : DevelopmentConfig,
#     'testing' : TestingConfig,
#     'production' : ProductionConfig,
#     'default' : DevelopmentConfig
# }
