# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys

from flask import current_app

sys.path.append("../geoip/")
sys.setrecursionlimit(10000000)

import geoip2.database
import traceback
import json

geo_city_reader = None
if not geo_city_reader:
    geo_city_reader = geoip2.database.Reader(current_app.config['GEO_LITE2CITY_FILE'])

geo_asn_reader = None
if not geo_asn_reader:
    geo_asn_reader = geoip2.database.Reader(current_app.config['GEO_LITE2ASN_FILE'])


def get_addr(ip='8.8.8.8'):
    # 获取ip的位置信息
    # 这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    try:
        response = geo_city_reader.city(ip)

        raw_json = json.dumps(response.raw, ensure_ascii=False)  # .replace("'","\\'")
        return raw_json, 1
    except Exception:
        error = traceback.format_exc()
        return '{}', 0


def get_asn(ip='8.8.8.8'):
    # 获取ip的自治系统号
    # 这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    reader = geoip2.database.Reader('app/geoip/GeoLite2-ASN.mmdb')
    try:
        response = reader.asn(ip)
        reader.close()
        raw_json = json.dumps(response.raw, ensure_ascii=False)  # .replace("'","\\'")
        return raw_json, 1
    except Exception:
        error = traceback.format_exc()
        return '{}', 0


if __name__ == "__main__":
    print(get_addr())
    print(get_asn())
