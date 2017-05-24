# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Email, Length, DataRequired, EqualTo
from app.model import User


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('自动登录')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('请输入密码：', validators=[DataRequired(), EqualTo('password2', message='两次输入密码必须相同。')])
    password2 = PasswordField('再次输入密码：', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮件地址已经注册。')