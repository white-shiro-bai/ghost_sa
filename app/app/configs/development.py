# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    app.configs.development

    development configuration.
    :copyright: (c) 2016 by the HDDATA Team.
"""

from app.configs.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):

    # Indicates that it is a dev environment
    DEBUG = True
    TESTING = False

    # 开发环境数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://developer:123456@10.237.43.115:3306/travelclouddev?charset=utf8'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = True

    WTF_CSRF_ENABLED = False

