##########################################
#
# 数据库管理工具
# author: TuYaxuan
# time: 2019/3/14
# 说明: flask_script flask_migrate
#
###########################################

from app import app, db, models
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='127.0.0.1', port=8000, use_debugger=True))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
