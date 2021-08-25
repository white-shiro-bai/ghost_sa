# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    鬼策接收数据模型
"""
from app.flaskr.models import ProjectModel, ProjectDeviceModel


class RequestData(object):
    """请求数据模型.
    """

    def __init__(self, project, remark) -> None:
        super().__init__()
        self.all_json = {}
        self.project = project
        self.remark = remark
        self.data = {}
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
        self.ip_is_good = 0
        self.ip_asn_is_good = 0
        self.created_at = ""
        self.updated_at = ""

        self.track_id = ""
        self.distinct_id = ""
        self.event = ""
        self.lib = ""
        self.type_ = ""

    def set_ua_properties(self, user_agent, ua_platform, ua_browser, ua_version):
        """设置ua属性.
        :param user_agent:
        :param ua_platform:
        :param ua_browser:
        :param ua_version:
        :return:
        """
        self.user_agent = user_agent
        self.ua_platform = ua_platform
        self.ua_browser = ua_browser
        self.ua_version = ua_version

    def set_connect_properties(self, connection, pragma, cache_control, accept, accept_encoding, accept_language):
        """设置连接属性.
        :param connection:
        :param pragma:
        :param cache_control:
        :param accept:
        :param accept_encoding:
        :param accept_language:
        :return:
        """
        self.connection = connection
        self.pragma = pragma
        self.cache_control = cache_control
        self.accept = accept
        self.accept_encoding = accept_encoding
        self.accept_language = accept_language

    def set_ip_properties(self, ip, ip_city, ip_asn, ip_is_goods, ip_asn_is_goods):
        """设置ip属性
        :param ip:
        :param ip_city:
        :param ip_asn:
        :param ip_is_goods:
        :param ip_asn_is_goods:
        :return:
        """
        self.ip = ip
        self.ip_city = ip_city
        self.ip_asn = ip_asn
        self.ip_is_good = ip_is_goods
        self.ip_asn_is_good = ip_asn_is_goods

    def set_url_properties(self, host,  url, referrer):
        """设置url属性.
        :param host:
        :param url:
        :param referrer:
        :return:
        """
        self.host = host
        self.url = url
        self.referrer = referrer

    def set_common_properties(self, track_id, distinct_id, event, lib, type_):
        """设置通用属性.
        :param track_id:
        :param distinct_id:
        :param event:
        :param lib:
        :param type_:
        :return:
        """

        self.track_id = track_id
        self.distinct_id = distinct_id
        self.event = event
        self.lib = lib
        self.type_ = type_

    def to_project_model(self):
        """将request_data转换成project_model
        :return:
        """
        project_model = ProjectModel()
        project_model.track_id = self.track_id
        project_model.distinct_id = self.distinct_id
        project_model.lib = self.lib
        project_model.event = self.event
        project_model.type_ = self.type_
        project_model.all_json = self.data
        project_model.host = self.host
        project_model.user_agent = self.user_agent
        project_model.ua_platform = self.ua_platform
        project_model.ua_browser = self.ua_browser
        project_model.user_agent = self.user_agent
        project_model.ua_platform = self.ua_platform
        project_model.ua_browser = self.ua_browser
        project_model.ua_version = self.ua_version
        project_model.ua_language = self.ua_language
        project_model.connection = self.connection
        project_model.pragma = self.pragma
        project_model.cache_control = self.cache_control
        project_model.accept = self.accept
        project_model.accept_encoding = self.accept_encoding
        project_model.accept_language = self.accept_language
        project_model.ip = self.ip
        project_model.ip_city = self.ip_city
        project_model.ip_asn = self.ip_asn
        project_model.url = self.url
        project_model.referrer = self.referrer
        project_model.remark = self.remark
        project_model.created_at = self.created_at

    def to_project_device_model(self):
        """将request_data转换成project_device
        :return:
        """
        project_device_model = ProjectDeviceModel()
        project_device_model.track_id = self.track_id
        project_device_model.distinct_id = self.distinct_id
        project_device_model.lib = self.lib
        project_device_model.event = self.event
        project_device_model.type_ = self.type_
        project_device_model.all_json = self.data
        project_device_model.host = self.host
        project_device_model.user_agent = self.user_agent
        project_device_model.ua_platform = self.ua_platform
        project_device_model.ua_browser = self.ua_browser
        project_device_model.user_agent = self.user_agent
        project_device_model.ua_platform = self.ua_platform
        project_device_model.ua_browser = self.ua_browser
        project_device_model.ua_version = self.ua_version
        project_device_model.ua_language = self.ua_language
        project_device_model.connection = self.connection
        project_device_model.pragma = self.pragma
        project_device_model.cache_control = self.cache_control
        project_device_model.accept = self.accept
        project_device_model.accept_encoding = self.accept_encoding
        project_device_model.accept_language = self.accept_language
        project_device_model.ip = self.ip
        project_device_model.ip_city = self.ip_city
        project_device_model.ip_asn = self.ip_asn
        project_device_model.url = self.url
        project_device_model.referrer = self.referrer
        project_device_model.remark = self.remark
        project_device_model.created_at = self.created_at
