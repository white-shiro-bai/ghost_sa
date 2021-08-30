# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys

from flask import current_app, _app_ctx_stack

sys.path.append("../geoip/")
sys.setrecursionlimit(10000000)

import geoip2.database
import json


class GeoCityReader(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def create_reader(self, app):
        app.logger.info('创建geo life city reader...')
        return geoip2.database.Reader(app.config['GEO_LITE2CITY_FILE'])

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'geo_city_reader'):
            ctx.geo_city_reader.close()
            current_app.logger.info('正常关闭geo_city_reader实例...')

    @property
    def reader(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'geo_city_reader'):
                ctx.geo_city_reader = self.create_reader()
            return ctx.geo_city_reader


class GeoAsnReader(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def create_reader(self, app):
        app.logger.info('创建geo life asn reader...')
        return geoip2.database.Reader(app.config['GEO_LITE2ASN_FILE'])

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'geo_asn_reader'):
            ctx.geo_asn_reader.close()
            current_app.logger.info('正常关闭geo_asn_reader实例...')

    @property
    def reader(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'geo_asn_reader'):
                ctx.geo_asn_reader = self.create_reader()
            return ctx.geo_asn_reader


def get_address(ip='8.8.8.8'):
    """使用geo2接口，获取ip对应地址信息.
    若获取失败，则返回相应空值{}，避免报错，丢失数据
    :param ip: ip
    :return: json对象，地址信息
    """
    response = None
    # 只获取第一条IP为ip_city信息，其它忽略
    first_ip = ip.split(', ')[0]
    try:
        response = current_app.geo_city_reader.city(first_ip)
    except Exception as e:
        current_app.logger.error(f'ip： {first_ip}获取地址失败，错误原因为: {e}')
    raw_json = response.raw if response else {}
    ret_code = 1 if response else 0
    return raw_json, ret_code


def get_asn(ip='8.8.8.8'):
    """使用geo2接口，获取asn对应地址信息.
        :param ip: ip
        :return: json对象，地址信息
    """
    response = None
    try:
        response = current_app.geo_asn_reader.asn(ip)
    except Exception as e:
        current_app.logger.error(f'ip： {ip}获取地ip asn失败，错误原因为: {e}')
    raw_json = response.raw if response else {}
    ret_code = 1 if response else 0
    return raw_json, ret_code


if __name__ == "__main__":
    print(get_address())
    print(get_asn())
