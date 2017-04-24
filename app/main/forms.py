# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class IndexForm(FlaskForm):
    pass


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    login = SubmitField('Login')
    logout = SubmitField('Logout')