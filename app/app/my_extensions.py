# -*- coding: utf-8 -*-
"""
    app.extensions

"""
from logging.handlers import SMTPHandler

from flask import json
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_plugins import PluginManager
from flask_sqlalchemy import (SQLAlchemy)
from flask_wtf.csrf import CSRFProtect

from app.component.kafka_op import CreateKafkaProducer
from app.utils.geo import GeoCityReader, GeoAsnReader

"""
    xiaowei.song 2016-7-13

    针对测试情况，重写Flask-sqlalchemy，默认开启第三方事物，不进行提交

    ref: https://gist.github.com/alexmic/7857543
"""

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()


# Provide a class to allow SSL (Not TLS) connection for mail handlers by overloading the emit() method
class MySMTPHandler(SMTPHandler):
    """
    xiaowei.song 2016-9-14

    自定义扩展SMTPHandler，使之支持ssl协议发送邮件
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, ssl=False):
        super(MySMTPHandler, self).__init__(mailhost, fromaddr, toaddrs, subject, credentials, secure)
        self.ssl = ssl

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            import smtplib
            from email.utils import formatdate
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT if not self.ssl else smtplib.SMTP_SSL_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self._timeout) if self.ssl else smtplib.SMTP(
                self.mailhost, port, timeout=self._timeout)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                ",".join(self.toaddrs),
                self.getSubject(record),
                formatdate(), msg)
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


#
# # Mail
# mail = Mail()
#
# # Redis
# redis_store = FlaskRedis()
#
# Debugtoolbar
# debugtoolbar = DebugToolbarExtension()

# Migrations
migrate = Migrate()

# PluginManager
plugin_manager = PluginManager()

# CSRF
csrf = CSRFProtect()

# cors
cors_ = CORS()

#
# # Celery
# celery = Celery("tosc", include=['app.tasks'])


class NonASCIIJsonEncoder(json.JSONEncoder):
    """
    xiaowei.song 2016-9-21

    重设json.dumps中参数设置，使之支持中文
    """

    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(NonASCIIJsonEncoder, self).__init__(**kwargs)


# # geo_city_reader
# geo_city_reader = GeoCityReader()
#
# # geo_asn_reader
# geo_asn_reader = GeoAsnReader()
#
# # kafka_producer
# kafka_producer = CreateKafkaProducer()
