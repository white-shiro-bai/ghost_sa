# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    鬼策接收数据模型
"""


class RequestData(object):
    """请求数据模型.
    """

    def __init__(self, project, remark) -> None:
        super().__init__()
        self.project = project
        self.remark = remark
        self.user_agent = ""
        self.host = ""
        self.connection = ""
        self.pragma = ""
        self.cache_control = ""
        self.accept = ""
        self.accept_encoding = ""
        self.accept_language = ""
        self.ip = ""
        self.ip_city = ""
        self.ip_asn = ""
        self.url = ""
        self.referrer = ""
        self.ua_platform = ""
        self.ua_browser = ""
        self.ua_version = ""
        self.ua_language = ""
        self.ip_is_good = ""
        self.ip_asn_is_good = ""
        self.created_at = ""
        self.updated_at = ""

