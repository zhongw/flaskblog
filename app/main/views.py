# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from .forms import IndexForm, LoginForm
from flask import render_template, abort, redirect, url_for, session, flash
from app.main import main


@main.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass


@main.route('/', methods=['POST','GET'])
def main():
    form = IndexForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        flash("You have set your name successfully!")
        return redirect(url_for('main.main'))

    return render_template("main.html", form=form, name=session.get('username'))
