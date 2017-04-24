# !/usr/bin/env python
#
# _*_ coding: utf-8 _*_
#
# Author: Juven Zhong
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