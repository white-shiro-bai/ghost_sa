# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    app.configs.testing
    ~~~~~~~~~~~~~~~~~~~
    This is the app's testing config.
"""

from app.configs.default import DefaultConfig


class TestingConfig(DefaultConfig):

    # Indicates that it is a testing environment
    DEBUG = False
    TESTING = True

    # 测试环境数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://cg_mall:cg_mall%40123@172.18.3.106:3306/ghost_test?charset=utf8'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # Security
    SECRET_KEY = "SecretKeyForSessionSigning"
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # 开启kafka接收数据
    USE_KAFKA = False

    # Error/Info Logging
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = False
    # 设置日志执行级别，应用中配置了相应的日志记录，禁用默认的
    LOGGER_HANDLER_POLICY = "never"

    # APP接口前缀
    APP_URL_PREFIX = "/app"

    # 设置用户操作日志开关
    SERVICE_LOG_ENABLED = True

    # Kafka的Topic
    KAFKA_TOPIC = 'events-tracking_test_cero'
