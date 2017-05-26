# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask_mail import Message
from flask import render_template
from . import mail
from threading import Thread
from manager import app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    """配置了MAIL_DEFAULT_SENDER，Message实例中可以不需要sender参数"""
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()