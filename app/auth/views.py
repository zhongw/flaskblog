# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask import render_template, redirect, url_for, request, flash
from app.auth import auth
from .forms import LoginForm
from flask_login import login_user, logout_user
from app.model import User


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.hello'))
        flash("用户名或密码错误，请重试。")
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash("成功退出。")
    return redirect(url_for('main.hello'))


@auth.route('/')
def index():
    return render_template('auth/index.html')