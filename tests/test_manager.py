# _*_ coding: utf-8 _*_
#
# Copyright (C) 2017 钟伟 <zhong.wei@qq.com>
# All rights reserved.
#
# Author: 钟伟 <zhong.wei@qq.com>
#

import unittest
from flask import current_app
from app import create_app


class ManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()


    def tearDown(self):
        self.app_ctx.pop()


    def test_app_exists(self):
        self.assertFalse(current_app is None)


    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])