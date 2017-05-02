# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Cloumn(db.Int, primary=True)
    username = db.Cloumn(db.String)
    password = db.Cloumn(db.String)


class Post(db.Model):
    pass