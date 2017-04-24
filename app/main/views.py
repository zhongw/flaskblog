# !/usr/bin/env python
#
# _*_ coding: utf-8 _*_
#
# Author: Juven Zhong
#

from .forms import IndexForm, LoginForm
from app.main import main


@main.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass