# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6,max=18)])
    login = SubmitField('Login')
    logout = SubmitField('Logout')


class PostForm(FlaskForm):
    body = TextAreaField("博客内容:", validators=[DataRequired()])
    submit = SubmitField("发布")