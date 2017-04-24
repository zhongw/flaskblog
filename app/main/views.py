# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from .forms import IndexForm, LoginForm
from app.main import main


@main.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass