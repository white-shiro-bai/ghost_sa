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
    SQLALCHEMY_DATABASE_URI = 'mysql://cg_mall:cg_mall%40123@172.18.3.106:3306/ghost_test?charset=utf8'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    WTF_CSRF_ENABLED = False

    # Kafka的Topic
    KAFKA_TOPIC = 'events-tracking_test_cero'

