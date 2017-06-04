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
from app.model import User


@main.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass


@main.route('/', methods=['POST','GET'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        flash("You have set your name successfully!")
        return redirect(url_for('main.index'))
    return render_template("main.html", form=form, name=session.get('username'))


@main.route('/user/<user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
