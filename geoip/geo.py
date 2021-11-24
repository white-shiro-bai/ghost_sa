# -*- coding: utf-8 -*-
#
#Date: 2021-09-18 16:29:59
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2021-11-24 16:52:09
#FilePath: \ghost_sa_github\geoip\geo.py
#
import sys
sys.path.append('./')
import geoip2.database
import traceback
import json
from configs import admin

def get_addr(ip='8.8.8.8', language=admin.ip_city_language, mode=admin.ip_city_mode):
    #获取ip的位置信息
    #这个文件在去这里下载对应的mmdb文件 https://dev.maxmind.com/geoip/geoip2/geolite2/
    reader = geoip2.database.Reader('geoip/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        reader.close()
        if mode == 'language':
            modify_data = {}
            if 'city' in response.raw:
                modify_data['city'] = {'geoname_id': response.raw['city']['geoname_id'] if 'geoname_id' in response.raw['city'] else None,"names": {}}
                for city_name_language in response.raw['city']['names']:
                    if city_name_language in language:
                        modify_data['city']['names'][city_name_language] = response.raw['city']['names'][city_name_language]
            if 'continent' in response.raw:
                modify_data['continent'] = {'geoname_id': response.raw['continent']['geoname_id'] if 'geoname_id' in response.raw['continent'] else None,"names": {}}
                for continent_name_language in response.raw['continent']['names']:
                    if continent_name_language in language:
                        modify_data['continent']['names'][continent_name_language] = response.raw['continent']['names'][continent_name_language]
            if 'country' in response.raw:
                modify_data['country'] = {'geoname_id': response.raw['country']['geoname_id'] if 'geoname_id' in response.raw['country'] else None,"names": {}}
                for country_name_language in response.raw['country']['names']:
                    if country_name_language in language:
                        modify_data['country']['names'][country_name_language] = response.raw['country']['names'][country_name_language]
            if 'location' in response.raw:
                modify_data['location'] = response.raw['location']
            if 'registered_country' in response.raw:
                modify_data['registered_country'] = {'geoname_id': response.raw['registered_country']['geoname_id'] if 'geoname_id' in response.raw['registered_country'] else None,"names": {}}
                for registered_country_name_language in response.raw['registered_country']['names']:
                    if registered_country_name_language in language:
                        modify_data['registered_country']['names'][registered_country_name_language] = response.raw['registered_country']['names'][registered_country_name_language]
            if 'subdivisions' in response.raw:
                modify_data['subdivisions'] = [{'geoname_id': response.raw['subdivisions'][0]['geoname_id'] if 'geoname_id' in response.raw['subdivisions'][0] else None,"names": {}}]
                for subdivisions_name_language in response.raw['subdivisions'][0]['names']:
                    if subdivisions_name_language in language:
                        modify_data['subdivisions'][0]['names'][subdivisions_name_language] = response.raw['subdivisions'][0]['names'][subdivisions_name_language]
            return json.dumps(modify_data, ensure_ascii=False), 1
        else:
            return json.dumps(response.raw, ensure_ascii=False), 1
    except Exception:
        error = traceback.format_exc()
        return '{}', 0

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
    print(get_addr(ip='124.115.214.179',mode='all'))
    print(get_addr(ip='124.115.214.179',language=['zh-CN','en'],mode='language'))
    print(get_asn())