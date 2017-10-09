# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 All rights reserved.
#
# @Time    : 2017-10-08 22:57
# @Author  : 钟伟 <zhong.wei@qq.com>
#

from flask import jsonify


def forbidden(message):
    """处理403错误：请求中发送的认证密令无权访问目标
    """
    response = jsonify({'error':'forbidden', 'message':message})
    response.status_code = 403
    return response
