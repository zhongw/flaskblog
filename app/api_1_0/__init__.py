# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# @Time    : 2017-10-08 22:50
# @Author  : 钟伟 <zhong.wei@qq.com>
#

from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, authentication, errors, posts
