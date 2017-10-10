# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 All rights reserved.
#
# @Time    : 2017-10-09 22:43
# @Author  : 钟伟 <zhong.wei@qq.com>
#

from flask_httpauth import HTTPBasicAuth
from flask_login import user_unauthorized
from app.model import AnonymousUser, User
from app.api_1_0.errors import forbidden
from app.api_1_0 import api
from flask import jsonify, g


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return user_unauthorized('Token不正确')
    return jsonify({'token': g.current_user.generate_token(expires_in=3600), 'expiration': 3600})


#@api.before_request
#@auth.login_required
#def before_request():
#    if not g.current_user.is_anonymous and g.current_user.confirmed:
#        return forbidden('Unconfirmed account')