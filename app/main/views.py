# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from .forms import IndexForm, LoginForm
from flask import render_template, abort, redirect, url_for, session, flash
from jinja2 import TemplateNotFound
from app.email import send_mail
from app.main import main
from manager import app


@main.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass


@main.route('/', methods=['POST','GET'])
def hello():
    form = IndexForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        flash("You have set your name successfully!")
        send_mail(app.config['FLASKY_MAIL_SENDER'], 'this is a testing mail', None)
        return redirect(url_for('main.hello'))

    try:
        return render_template("hello.html", form=form, name=session.get('username'))
    except TemplateNotFound:
        abort(404)