# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

from flask import Blueprint
main = Blueprint('main', __name__)


from . import views, forms
from app.model import Permission


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

