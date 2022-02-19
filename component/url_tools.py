# -*- coding: utf-8 -*-
#
#Date: 2021-09-18 16:29:59
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-02-19 19:56:23
#FilePath: \ghost_sa_github\component\url_tools.py
#
import sys
sys.path.append("./")
from flask import request
from configs.export import write_to_log
from geoip.geo import get_addr,get_asn
from configs import admin
import urllib


def get_url_params(params,default=None,log_error=False):
    # Extract params from any type of request as possible as support. 
    # It was designed to enhance compatibility in corporation with engineer who knows requests very well.
    # Order :  JSON > POST(form) > GET (args) > POST/GET with wrong data > Beacon > Other type of data
    # Beacon support is provided by https://github.com/phillip2019/
    try:
        got_json = request.json
    except:
        got_json = None
    v = None
    if got_json:
        if params in got_json:
            v = got_json[params]
    if v == '' or not v:
        if request.method == 'POST':
            v = request.form.get(params)
        elif request.method == 'GET':
            v = request.args.get(params)
        if request.method == 'POST' and not v:
            v = request.args.get(params)
        elif request.method == 'GET' and not v:
            v = request.form.get(params)
        if 'text/plain' in request.headers.get('CONTENT-TYPE', '') and not v:
            play_load_str = request.data.decode('utf-8')
            v = dict(urllib.parse.parse_qsl(play_load_str)).get(params)
        elif not v:
            play_load_str = request.data.decode('utf-8')
            v = dict(urllib.parse.parse_qsl(play_load_str)).get(params)
    if v and v != '':
        return v
    else:
        if log_error is True:
            write_to_log(filename='url_tools',defname='get_url_params',result='params:'+str(params)+';')
        return default

def get_ip():
    if request.headers.get('X-Forwarded-For') is None:
        ip = request.remote_addr#服务器直接暴露
    else:
        ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    return ip


def get_req_info():
    remark =  request.args.get('remark','normal')
    User_Agent = request.headers.get('User-Agent')[0:767] if request.headers.get('User-Agent') else None#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
    if get_url_params('user_agent'):
        User_Agent = get_url_params('user_agent')
    if User_Agent and User_Agent !='' and any([pt in User_Agent.lower() for pt in admin.bot_list]):
        remark = 'spider'
    Host = request.headers.get('Host') #: 10.16.5.241:5000
    if get_url_params('host'):
        Host = get_url_params('host')
    Connection = request.headers.get('Connection')#: keep-alive
    Pragma = request.headers.get('Pragma')#: no-cache
    Cache_Control = request.headers.get('Cache-Control')#: no-cache
    Accept = request.headers.get('Accept')[0:254] if request.headers.get('Accept') else None#: image/webp,image/apng,image/*,*/*;q=0.8
    Accept_Encoding = request.headers.get('Accept-Encoding')[0:254] if request.headers.get('Accept-Encoding') else None#: gzip, deflate
    Accept_Language = request.headers.get('Accept-Language')[0:254] if request.headers.get('Accept-Language') else None#: zh-CN,zh;q=0.9
    ua_platform = request.user_agent.platform #客户端操作系统
    ua_browser = request.user_agent.browser #客户端的浏览器
    ua_version = request.user_agent.version #客户端浏览器的版本
    ua_language = request.user_agent.language #客户端浏览器的语言
    url = request.url
    if get_url_params('request_uri'):
        url = get_url_params('request_uri')
    if get_url_params('http_x_forward_for') and get_url_params('http_x_forward_for') != '' and get_url_params('http_x_forward_for').count('.')==3:
        ip = get_url_params('http_x_forward_for')
    elif get_url_params('remote_addr') and get_url_params('remote_addr') != '' and get_url_params('remote_addr').count('.')==3:
        ip = get_url_params('remote_addr')
    elif get_url_params('ip') and get_url_params('ip') != '' and get_url_params('ip').count('.')==3:
        ip = get_url_params('ip')
    elif request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    else:
        ip = request.remote_addr#服务器直接暴露
    # ip = '124.115.214.179' #测试西安bug
    # ip = '36.5.99.68' #测试安徽bug
    ip_city,ip_is_good = get_addr(ip)
    ip_asn,ip_asn_is_good = get_asn(ip)
    referrer = request.referrer[0:2047] if request.referrer else None
    if get_url_params('http_referrer') and get_url_params('http_referrer')!= '$http_referrer' :
        referrer = get_url_params('http_referrer')[0:2047]
    elif get_url_params('http_referer') and get_url_params('http_referer')!= '$http_referer' :
        referrer = get_url_params('http_referer')[0:2047]
    return {'remark':remark,'User_Agent':User_Agent,'Host':Host,'Connection':Connection,'Pragma':Pragma,'Cache_Control':Cache_Control,'Accept':Accept,'Accept_Encoding':Accept_Encoding,'Accept_Language':Accept_Language,'ua_platform':ua_platform,'ua_browser':ua_browser,'ua_version':ua_version,'ua_language':ua_language,'url':url,'ip':ip,'ip_city':ip_city,'ip_is_good':ip_is_good,'ip_asn':ip_asn,'ip_asn_is_good':ip_asn_is_good,'referrer':referrer}