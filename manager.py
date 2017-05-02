# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask_script import Manager
from app import db, create_app
from flask_migrate import Migrate, MigrateCommand

app = create_app('testing')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()