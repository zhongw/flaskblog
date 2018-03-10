# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from .forms import PostForm, LoginForm
from flask import render_template, abort, redirect, url_for, session, flash
from app.main import main
from app.model import User, Post
from flask_login import current_user
from app import db


@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass


@main.route('/', methods=['GET'])
def index():
    form = PostForm()
    author = current_user._get_current_object()
    if form.validate_on_submit():
        body = form.body.data
        post = Post(body=body, author_id=author.id)
        db.session.add(post)
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.create_date.desc()).all()
    return render_template("index.html", form=form, posts=posts)


@main.route('/user/<user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/post/<id>')
def post(id):
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.author_id)
    return render_template('post.html', post=post, author=user)


@main.errorhandler(404)
def page_not_found(e):
    abort(404)
    return render_template("404.html"), 404