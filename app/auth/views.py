# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask import render_template, redirect, url_for, request, flash
from app.auth import auth
from .forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from app.model import User
from app import db
from app.email import send_mail


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("用户名或密码错误，请重试。")
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash("成功退出。")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        send_mail(user.email, '请验证你的邮件地址', 'auth/email/confirm', user=user, token=token)
        flash('邮件验证链接已经发送到<b>{0}</b>, 请查收。'.format(form.email.data))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/')
def index():
    return render_template('auth/index.html')


@auth.before_app_request
def before_request():
    """在每次请求前运行"""
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.email_confirmed \
            and request.endpoint[:5] != 'auth.'  \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm')
@login_required
def confirm():
    token = request.args.get('token')
    if current_user.email_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_email(token):
        flash('你的邮箱地址已经验证，谢谢。')
    else:
        flash('验证连接地址无效或已过期。')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.email_confirmed:
        return redirect(url_for('main.index'))
    return 'not valid'