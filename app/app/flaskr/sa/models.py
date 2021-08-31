# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    xiaowei.song 2016-11-06
    模型类文件
"""

from sqlalchemy.dialects.mysql import JSON

from app.my_extensions import db


class ProjectModel(db.Model):
    __abstract__ = True
    __tablename__ = 'project'

    track_id = db.Column(db.BigInteger, primary_key=True)
    distinct_id = db.Column(db.String(64), primary_key=True)
    lib = db.Column(db.String(255))
    event = db.Column(db.String(255))
    type_ = db.Column('type', db.String(255))
    all_json = db.Column(db.JSON())
    host = db.Column(db.String(255))
    user_agent = db.Column(db.String(2048))
    ua_platform = db.Column(db.String(1024))
    ua_browser = db.Column(db.String(1024))
    ua_version = db.Column(db.String(1024))
    ua_language = db.Column(db.String(1024))
    connection = db.Column(db.String(255))
    pragma = db.Column(db.String(255))
    cache_control = db.Column(db.String(255))
    accept = db.Column(db.String(255))
    accept_encoding = db.Column(db.String(255))
    accept_language = db.Column(db.String(255))
    ip = db.Column(db.String(512))
    ip_city = db.Column(db.JSON())
    ip_asn = db.Column(db.JSON())
    url = db.Column(db.Text())
    referrer = db.Column(db.String(2048))
    remark = db.Column(db.String(255))
    created_at = db.Column(db.BigInteger)
    date_ = db.Column('date', db.Date)
    hour = db.Column(db.Integer)


class ProjectDeviceModel(db.Model):
    __abstract__ = True
    __tablename__ = 'project_device'

    distinct_id = db.Column(db.String(64), primary_key=True)
    lib = db.Column(db.String(255))
    device_id = db.Column(db.String(255))
    manufacturer = db.Column(db.String(200))
    model = db.Column(db.String(200))
    os = db.Column(db.String(200))
    os_version = db.Column(db.String(200))
    screen_width = db.Column(db.Integer)
    screen_height = db.Column(db.Integer)
    network_type = db.Column(db.String(32))
    user_agent = db.Column(db.String(2048))
    ua_platform = db.Column(db.String(200))
    ua_browser = db.Column(db.String(200))
    ua_version = db.Column(db.String(200))
    ua_language = db.Column(db.String(200))
    connection = db.Column(db.String(255))
    pragma = db.Column(db.String(255))
    cache_control = db.Column(db.String(255))
    accept = db.Column(db.String(255))
    accept_encoding = db.Column(db.String(255))
    accept_language = db.Column(db.String(255))
    ip = db.Column(db.String(512))
    ip_city = db.Column(JSON)
    ip_asn = db.Column(JSON)
    wifi = db.Column(db.String(20))
    app_version = db.Column(db.String(255))
    carrier = db.Column(db.String(255))
    referrer = db.Column(db.String(2048))
    referrer_host = db.Column(db.String(512))
    bot_name = db.Column(db.String(255))
    browser = db.Column(db.String(128))
    browser_version = db.Column(db.String(128))
    is_login_id = db.Column(db.String(32))
    screen_orientation = db.Column(db.String(64))
    gps_latitude = db.Column(db.Numeric(11, 7))
    gps_longitude = db.Column(db.Numeric(11, 7))
    first_visit_time = db.Column(db.DateTime)
    first_referrer = db.Column(db.String(2048))
    first_referrer_host = db.Column(db.String(512))
    first_browser_language = db.Column(db.String(128))
    first_browser_charset = db.Column(db.String(128))
    first_search_keyword = db.Column(db.String(768))
    first_traffic_source_type = db.Column(db.String(255))
    utm_content = db.Column(db.String(768), index=True)
    utm_campaign = db.Column(db.String(768), index=True)
    utm_medium = db.Column(db.String(768), index=True)
    utm_term = db.Column(db.String(768), index=True)
    utm_source = db.Column(db.String(768), index=True)
    latest_utm_content = db.Column(db.String(768))
    latest_utm_campaign = db.Column(db.String(768))
    latest_utm_medium = db.Column(db.String(768))
    latest_utm_term = db.Column(db.String(768))
    latest_utm_source = db.Column(db.String(768))
    latest_referrer = db.Column(db.String(2048))
    latest_referrer_host = db.Column(db.String(512))
    latest_search_keyword = db.Column(db.String(768))
    latest_traffic_source_type = db.Column(db.String(255))
    created_at = db.Column(db.BigInteger, index=True)
    updated_at = db.Column(db.BigInteger)


class ProjectUserModel(db.Model):
    __abstract__ = True
    __tablename__ = 'project_user'

    distinct_id = db.Column(db.String(64), index=True, primary_key=True)
    lib = db.Column(db.String(255), primary_key=True)
    map_id = db.Column(db.String(200), index=True, primary_key=True)
    original_id = db.Column(db.String(255), index=True, primary_key=True)
    user_id = db.Column(db.String(255))
    all_user_profile = db.Column(db.String(255))
    created_at = db.Column(db.BigInteger)
    updated_at = db.Column(db.BigInteger)


class ProjectPropertiesModel(db.Model):
    __abstract__ = True
    __tablename__ = 'project_properties'

    lib = db.Column(db.String(255), primary_key=True)
    remark = db.Column(db.String(255), primary_key=True)
    event = db.Column(db.String(255), primary_key=True)
    properties = db.Column(JSON())
    properties_len = db.Column(db.Integer)
    lastinsert_at = db.Column(db.Integer)
    total_count = db.Column(db.BigInteger)
    access_control_threshold = db.Column(db.Integer)
    created_at = db.Column(db.BigInteger)
    updated_at = db.Column(db.BigInteger)
