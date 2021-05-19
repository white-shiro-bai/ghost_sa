# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)

import geoip2.database
import traceback
import json
import pprint

def get_addr(ip='8.8.8.8'):
    #获取ip的位置信息
    #这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    reader = geoip2.database.Reader('geoip/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        reader.close()
        raw_json = json.dumps(response.raw,ensure_ascii=False)#.replace("'","\\'")
        return raw_json,1
    except Exception:
        error = traceback.format_exc()
        return '{}',0

def get_asn(ip='8.8.8.8'):
    #获取ip的自治系统号
    #这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    reader = geoip2.database.Reader('geoip/GeoLite2-ASN.mmdb')
    try:
        response = reader.asn(ip)
        reader.close()
        raw_json = json.dumps(response.raw,ensure_ascii=False)#.replace("'","\\'")
        return raw_json,1
    except Exception:
        error = traceback.format_exc()
        return '{}',0
if __name__ == "__main__":
    print(get_addr())
    print(get_asn())