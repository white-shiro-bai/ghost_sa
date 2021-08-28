# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    鬼策接收数据模型
"""
import json
import time

from app.flaskr.models import ProjectModel, ProjectDeviceModel, ProjectPropertiesModel, ProjectUserModel


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

        self.track_id = ""
        self.distinct_id = ""
        self.event = ""
        self.lib = ""
        self.type_ = ""

        self.device_id = ""
        self.manufacturer = ""
        self.model = ""
        self.os = ""
        self.os_version = ""
        self.screen_width = ""
        self.screen_height = ""
        self.network_type = ""
        self.is_first_day = ""
        self.is_first_time = ""
        self.wifi = ""
        self.app_version = ""
        self.carrier = ""
        self.referrer_host = ""
        self.bot_name = ""
        self.browser = ""
        self.browser_version = ""
        self.is_login_id = ""
        self.screen_orientation = ""
        self.gps_latitude = ""
        self.gps_longitude = ""
        self.utm_content = ""
        self.utm_campaign = ""
        self.utm_medium = ""
        self.utm_term = ""
        self.utm_source = ""
        self.latest_utm_content = ""
        self.latest_utm_campaign = ""
        self.latest_utm_medium = ""
        self.latest_utm_term = ""
        self.latest_utm_source = ""
        self.latest_referrer = ""
        self.latest_referrer_host = ""
        self.latest_search_keyword = ""
        self.latest_traffic_source_type = ""
        self.first_visit_time = ""
        self.first_referrer = ""
        self.first_referrer_host = ""
        self.first_browser_language = ""
        self.first_browser_charset = ""
        self.first_search_keyword = ""
        self.first_traffic_source_type = ""

        self.map_id = ''
        self.original_id = ''
        self.user_id = ''
        self.all_user_profile = ''

        ct = time.time()
        local_time = time.localtime(ct)
        created_at = int(ct)
        dt = time.strftime("%Y-%m-%d", local_time)
        hour = int(time.strftime("%H", local_time))
        self.created_at = created_at
        self.updated_at = created_at
        self.dt = dt
        self.hour = hour

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

    def set_other_properties(self):
        """从properties中解析其它属性.
        :return:
        """
        data = self.data
        data_properties = data.get('properties', {})
        self.device_id = data_properties.get('$device_id')
        self.manufacturer = data_properties.get('$manufacturer')
        self.model = data_properties.get('$model')
        self.os = data_properties.get('$os')
        self.os_version = data_properties.get('$os_version')
        self.screen_width = data_properties.get('$screen_width')
        self.screen_height = data_properties.get('$screen_height')
        self.network_type = data_properties.get('$network_type')
        self.is_first_day = data_properties.get('$is_first_day')
        self.is_first_time = data_properties.get('$is_first_time')
        self.wifi = data_properties.get('$wifi')
        self.app_version = data_properties.get('$app_version')
        self.carrier = data_properties.get('$carrier')
        self.referrer = data_properties.get('$referrer')
        self.referrer_host = data_properties.get('$referrer_host')
        self.bot_name = data_properties.get('$bot_name')
        self.browser = data_properties.get('$browser')
        self.browser_version = data_properties.get('$browser_version')
        self.is_login_id = data_properties.get('$is_login_id')
        self.screen_orientation = data_properties.get('$screen_orientation')
        self.gps_latitude = data_properties.get('$latitude')
        self.gps_longitude = data_properties.get('$longitude')
        self.utm_content = data_properties.get('$utm_content')
        self.utm_campaign = data_properties.get('$utm_campaign')
        self.utm_medium = data_properties.get('$utm_medium')
        self.utm_term = data_properties.get('$utm_term')
        self.utm_source = data_properties.get('$utm_source')
        self.latest_utm_content = data_properties.get('$latest_utm_content')
        self.latest_utm_campaign = data_properties.get('$latest_utm_campaign')
        self.latest_utm_medium = data_properties.get('$latest_utm_medium')
        self.latest_utm_term = data_properties.get('$latest_utm_term')
        self.latest_utm_source = data_properties.get('$latest_utm_source')
        self.latest_referrer = data_properties.get('$latest_referrer')
        self.latest_referrer_host = data_properties.get('$latest_referrer_host')
        self.latest_search_keyword = data_properties.get('$latest_search_keyword')
        self.latest_traffic_source_type = data_properties.get('$latest_traffic_source_type')
        self.first_visit_time = data_properties.get('$first_visit_time')
        self.first_referrer = data_properties.get('$first_referrer')
        self.first_referrer_host = data_properties.get('$first_referrer_host')
        self.first_browser_language = data_properties.get('$first_browser_language')
        self.first_browser_charset = data_properties.get('$first_browser_charset')
        self.first_search_keyword = data_properties.get('$first_search_keyword')
        self.first_traffic_source_type = data_properties.get('$first_traffic_source_type')

        # 用户个人信息使用
        self.map_id = self.data.get('map_id', '')
        self.original_id = self.data.get('original_id', '')
        if 'userId' in data_properties:
            self.user_id = data_properties.get('userId')
        elif 'user_id' in data_properties:
            self.user_id = data_properties.get('user_id')
        elif 'uid' in data_properties:
            self.user_id = data_properties.get('uid')
        self.all_user_profile = json.dumps(data_properties) if self.type_ == 'profile_set' else ''

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
        project_model.date_ = self.dt
        project_model.hour = self.hour
        return project_model

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
        project_device_model.dt = self.dt
        project_device_model.hour = self.hour
        return project_device_model

    def to_project_properties_model(self):
        """将request_data转换成project_properties
        :return:
        """
        project_properties_model = ProjectPropertiesModel()
        project_properties_model.lib = self.lib
        project_properties_model.event = self.event
        project_properties_model.remark = self.remark
        data_properties = self.data.get('properties')
        project_properties_model.properties = data_properties.keys()
        project_properties_model.properties_len = len(data_properties.keys())
        project_properties_model.total_count = 1
        project_properties_model.created_at = self.created_at
        project_properties_model.updated_at = self.created_at
        return project_properties_model

    def to_project_user_model(self):
        """将request_data转换成project_user
        :return:
        """
        project_user_model = ProjectUserModel()
        project_user_model.distinct_id = self.distinct_id
        project_user_model.lib = self.lib
        project_user_model.map_id = self.map_id
        project_user_model.original_id = self.original_id
        project_user_model.user_id = self.user_id
        project_user_model.all_user_profile = self.all_user_profile
        project_user_model.created_at = self.created_at
        project_user_model.updated_at = self.created_at
        return project_user_model

    def update_project_device_model(self, project_device_model_db):
        if self.ip_is_good == 1:
            project_device_model_db.ip_city = self.ip_city

        if self.ip_asn_is_good == 1:
            project_device_model_db.ip_asn = self.ip_asn

        if self.lib:
            project_device_model_db.lib = self.lib

        if self.device_id:
            project_device_model_db.device_id = self.device_id

        if self.ua_platform:
            project_device_model_db.ua_platform = self.ua_platform

        if self.ua_browser:
            project_device_model_db.ua_browser = self.ua_browser

        if self.ua_version:
            project_device_model_db.ua_version = self.ua_version

        if self.ua_language:
            project_device_model_db.ua_language = self.ua_language

        if self.manufacturer:
            project_device_model_db.manufacturer = self.manufacturer

        if self.model:
            project_device_model_db.model = self.model

        if self.os:
            project_device_model_db.os = self.os

        if self.os_version:
            project_device_model_db.os_version = self.os_version

        if self.screen_width:
            project_device_model_db.screen_width = self.screen_width

        if self.screen_height:
            project_device_model_db.screen_height = self.screen_height

        if self.network_type:
            project_device_model_db.network_type = self.network_type

        if self.user_agent:
            project_device_model_db.user_agent = self.user_agent

        if self.accept_language:
            project_device_model_db.accept_language = self.accept_language

        if self.ip:
            project_device_model_db.ip = self.ip

        if self.wifi or self.wifi is False:
            project_device_model_db.wifi = self.wifi

        if self.app_version:
            project_device_model_db.app_version = self.app_version

        if self.carrier:
            project_device_model_db.carrier = self.carrier

        if self.referrer:
            project_device_model_db.referrer = self.referrer

        if self.referrer_host:
            project_device_model_db.referrer_host = self.referrer_host

        if self.bot_name:
            project_device_model_db.bot_name = self.bot_name

        if self.browser:
            project_device_model_db.browser = self.browser

        if self.browser_version:
            project_device_model_db.browser_version = self.browser_version

        if self.is_login_id:
            project_device_model_db.is_login_id = self.is_login_id

        if self.screen_orientation:
            project_device_model_db.screen_orientation = self.screen_orientation

        if self.gps_latitude:
            project_device_model_db.gps_latitude = self.gps_latitude

        if self.gps_longitude:
            project_device_model_db.gps_longitude = self.gps_longitude

        if self.first_visit_time:
            project_device_model_db.first_visit_time = self.first_visit_time

        if self.first_referrer:
            project_device_model_db.first_referrer = self.first_referrer

        if self.first_referrer_host:
            project_device_model_db.first_referrer_host = self.first_referrer_host

        if self.first_browser_language:
            project_device_model_db.first_browser_language = self.first_browser_language

        if self.first_browser_charset:
            project_device_model_db.first_browser_charset = self.first_browser_charset

        if self.first_search_keyword:
            project_device_model_db.first_search_keyword = self.first_search_keyword

        if self.first_traffic_source_type:
            project_device_model_db.first_traffic_source_type = self.first_traffic_source_type

        if self.utm_content:
            project_device_model_db.utm_content = self.utm_content

        if self.utm_campaign:
            project_device_model_db.utm_campaign = self.utm_campaign

        if self.utm_medium:
            project_device_model_db.utm_medium = self.utm_medium

        if self.utm_term:
            project_device_model_db.utm_term = self.utm_term

        if self.utm_source:
            project_device_model_db.utm_source = self.utm_source

        if self.latest_utm_content:
            project_device_model_db.latest_utm_content = self.latest_utm_content

        if self.latest_utm_campaign:
            project_device_model_db.latest_utm_campaign = self.latest_utm_campaign

        if self.latest_utm_medium:
            project_device_model_db.latest_utm_medium = self.latest_utm_medium

        if self.latest_utm_term:
            project_device_model_db.latest_utm_term = self.latest_utm_term

        if self.latest_utm_source:
            project_device_model_db.latest_utm_source = self.latest_utm_source

        if self.latest_referrer:
            project_device_model_db.latest_referrer = self.latest_referrer

        if self.latest_referrer_host:
            project_device_model_db.latest_referrer_host = self.latest_referrer_host

        if self.latest_search_keyword:
            project_device_model_db.latest_search_keyword = self.latest_search_keyword

        if self.latest_traffic_source_type:
            project_device_model_db.latest_traffic_source_type = self.latest_traffic_source_type

        project_device_model_db.date_ = self.dt
        project_device_model_db.hour = self.hour
        project_device_model_db.updated_at = self.updated_at

    def update_project_properties_model(self, project_properties_model_db):
        if project_properties_model_db.properties_len < len(self.data.keys()):
            project_properties_model_db.properties_len = len(self.data.keys())
            project_properties_model_db.properties = self.data.keys()

        project_properties_model_db.total_count += 1
        project_properties_model_db.lastinsert_at = self.updated_at

    def to_kafka_msg(self):
        kafka_msg = {
            'group': 'event_track',
            'timestamp': self.created_at,
            'data': {
                'project': self.project,
                'data_decode': self.data,
                'User_Agent': self.user_agent,
                'Host': self.host,
                'Connection': self.connection,
                'Cache_Control': self.cache_control,
                'Accept': self.accept,
                'Accept_Encoding': self.accept_encoding,
                'Accept_Language': self.accept_language,
                'ip': self.ip,
                'ip_city': self.ip_city,
                'ip_asn': self.ip_asn,
                'url': self.url,
                'referrer': self.referrer,
                'remark': self.remark,
                'ua_platform': self.ua_platform,
                'ua_browser': self.ua_browser,
                'ua_version': self.ua_version,
                'ua_language': self.ua_language,
                'ip_is_good': self.ip_is_good,
                'ip_asn_is_goods': self.ip_asn_is_good,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
            }
        }
        return kafka_msg









