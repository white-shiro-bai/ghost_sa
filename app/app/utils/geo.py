# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys

from flask import current_app, g

sys.path.append("../geoip/")
sys.setrecursionlimit(10000000)

import geoip2.database
import json


def get_geo_city_reader():
    """全局注册geo_city_reader
    :return:
    """
    if 'geo_city_reader' not in g:
        g.geo_city_reader = geoip2.database.Reader(current_app.config['GEO_LITE2CITY_FILE'])

    return g.geo_city_reader


def get_geo_asn_reader():
    """全局注册geo_city_reader
    :return:
    """
    if 'geo_asn_reader' not in g:
        g.geo_asn_reader = geoip2.database.Reader(current_app.config['GEO_LITE2ASN_FILE'])

    return g.geo_asn_reader


def get_address(ip='8.8.8.8'):
    """使用geo2接口，获取ip对应地址信息.
    若获取失败，则返回相应空值{}，避免报错，丢失数据
    :param ip: ip
    :return: json对象，地址信息
    """
    response = None
    try:
        response = get_geo_city_reader().city(ip)
    except Exception as e:
        current_app.logger.error(f'ip： {ip}获取地址失败，错误原因为: ', e)
    raw_json = json.dumps(response.raw if response else {}, ensure_ascii=False)
    ret_code = 1 if response else 0
    return raw_json, ret_code


def get_asn(ip='8.8.8.8'):
    """使用geo2接口，获取asn对应地址信息.
        :param ip: ip
        :return: json对象，地址信息
    """
    response = None
    try:
        response = get_geo_asn_reader.asn(ip)
    except Exception as e:
        current_app.logger.error(f'ip： {ip}获取地ip asn失败，错误原因为: ', e)
    raw_json = json.dumps(response.raw if response else {}, ensure_ascii=False)
    ret_code = 1 if response else 0
    return raw_json, ret_code


if __name__ == "__main__":
    print(get_address())
    print(get_asn())
