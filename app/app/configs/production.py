# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    app.configs.production

    production configuration.
"""
import os

from app.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):

    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'mysql://tosc:w8Jr3RGy@localhost/tosc?charset=utf8'

    # 不输出SQL语句
    SQLALCHEMY_ECHO = False

    # 系统密钥
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = os.urandom(24)

    # You can generate the WTF_CSRF_SECRET_KEY the same way as you have
    # generated the SECRET_KEY. If no WTF_CSRF_SECRET_KEY is provided, it will
    # use the SECRET_KEY.
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # TravelSky mail 开启SSL保护，关闭TLS，使用465端口
    MAIL_SERVER = "mail.travelsky.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "teamwork@travelsky.com"
    MAIL_PASSWORD = "12345abc"
    MAIL_DEFAULT_SENDER = ("Default Sender", "teamwork@travelsky.com")
    # 系统管理员，接收相关系统错误日志邮件
    ADMINS = ["teamwork@travelsky.com"]

    # Error/Info Logging
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = True

    # The filename for the info and error logs. The logfiles are stored at
    # tosc/logs
    INFO_LOG = "info"
    ERROR_LOG = "error"

    # 按照文件大小分割参数配置
    MAX_BYTES = 100000
    BACKUP_COUNT = 10

    # 按照时间分割参数配置
    BACKUP_WHEN = "midnight"
    BACKUP_COUNT = 62
    # 备份配置文件后缀名
    BACKUP_SUFFIX = "%Y%m%d-%H%M.log"

    # 日志格式化参数配置
    DEBUG_FORMATTER = "%(asctime)s %(levelname)s %(message)s"
    INFO_FORMATTER = "%(asctime)s %(levelname)s %(message)s"
    ERROR_FORMATTER = "%(asctime)s %(levelname)s %(module)s 6%(process)d %(thread)d %(message)s"

    # 设置用户操作日志开关
    SERVICE_LOG_ENABLED = False
