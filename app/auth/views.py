# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask import render_template
from app.auth import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/')
def index():
    return 'hello login', 200