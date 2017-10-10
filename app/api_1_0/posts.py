# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 All rights reserved.
#
# @Time    : 2017-10-10 22:32
# @Author  : 钟伟 <zhong.wei@qq.com>
#

from flask import jsonify
from app.api_1_0 import api
from app.model import Post


@api.route('/posts/')
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({post.to_json()})
