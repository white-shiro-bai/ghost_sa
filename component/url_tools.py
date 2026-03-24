# -*- coding: utf-8 -*-
#
#Date: 2021-09-18 16:29:59
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-07-06 20:14:23
#FilePath: \ghost_sa_github_cgq\component\url_tools.py
#
import sys
sys.path.append("./")
from flask import request
from configs.export import write_to_log
from geoip.geo import get_addr,get_asn
from configs import admin
from component.public_func import key_counter
from urllib.parse import urlparse
import ipaddress
import urllib
import base64
import json
import gzip
import string

def sa_decode(params):
    de64 = base64.b64decode(urllib.parse.unquote(params))
    if admin.gzip_first is True:
        try:
            pending_data = json.loads(gzip.decompress(de64))
            return pending_data
        except:
            pending_data = json.loads(de64)
            return pending_data
    else:
        try:
            pending_data = json.loads(de64)
            return pending_data
        except:
            pending_data = json.loads(gzip.decompress(de64))
            return pending_data

def force_to_bool(key):
    if any(pt == str(key).lower() for pt in ['true','yes','1','on']):
        return True
    elif any(pt == str(key).lower() for pt in ['false','no','0','off']):
        return False
    else:
        return False

def bool_to_str(key):
    if isinstance(key,bool):
        if key is True:
            return 'True'
        elif key is False:
            return 'False'
    elif isinstance(key,str):
        if key.lower() in ['true','yes','1','on']:
            return 'True'
        elif key.lower() in ['false','no','0','off']:
            return 'False'
        else:
            return None
    else:
        return None

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
        if admin.bot_override is False or get_url_params('no_bot') != admin.admin_password : # mark spider if not allow override or password is wrong.
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
    ip_group={'internet':{},'internal':{}}
    ip_key_list = ['X-Forwarded-For','X-Original-Forwarded-For','X-True-Ip','X-Client-Ip','Wl-Proxy-Client-Ip','Proxy-Client-IP','X-Real-IP','HTTP_CLIENT_IP']
    if get_url_params('http_x_forward_for') and get_url_params('http_x_forward_for') != '' and get_url_params('http_x_forward_for').count('.')==3:
        ip = get_url_params('http_x_forward_for')
    elif get_url_params('remote_addr') and get_url_params('remote_addr') != '' and get_url_params('remote_addr').count('.')==3:
        ip = get_url_params('remote_addr')
    elif get_url_params('ip') and get_url_params('ip') != '' and get_url_params('ip').count('.')==3:
        ip = get_url_params('ip')
    else:
        for header_key in ip_key_list:
            #处理反向代理和其他WAF带过来的头信息
            pending_ip = request.headers.get(header_key).split(',')[0].strip() if request.headers.get(header_key) else None
            if pending_ip and len(pending_ip.split('.'))==4:
                is_good_ip = get_addr(pending_ip)[1]
                if is_good_ip == 1 :
                    ip_group = key_counter(group=ip_group,keytype='internet',key=pending_ip)
                elif is_good_ip == 0 :
                    ip_group = key_counter(group=ip_group,keytype='internal',key=pending_ip)
        ip = request.remote_addr#服务器直接暴露
        is_good_ip = get_addr(ip)[1]
        if is_good_ip == 1 :
            ip_group = key_counter(group=ip_group,keytype='internet',key=ip)
        elif is_good_ip == 0 :
            ip_group = key_counter(group=ip_group,keytype='internal',key=ip)
        if len(ip_group['internet'])>0:
            ip = max(ip_group['internet'], key=lambda x:ip_group['internet'][x])
        else:
            ip = max(ip_group['internal'], key=lambda x:ip_group['internal'][x])
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

def is62hex(text):
    text = str(text)
    for i in text:
        if i not in string.hexdigits + string.ascii_letters :
            return 0,i
    return 1,None

def normalize_host(host):
    #"""
    #Normalize host for whitelist comparison:
    #- lowercase
    #- strip surrounding spaces
    #- remove trailing dot
    #- remove port (standard or non-standard)
    #- support IPv4 / IPv6 / domain
    #Thanks https://github.com/LeaveerWang provide code. 
    #"""
    if not host:
        return host

    h = host.strip().lower()

    # 兼容无 netloc 的情况
    if "://" in h:
        parsed = urlparse(h)
        h = parsed.netloc or parsed.path  

    # 去掉末尾的点（FQDN）
    if h.endswith('.'):
        h = h[:-1]

    # 处理 IPv6 (带 [] 的情况) 
    if h.startswith('['):
        # 格式: [IPv6]:port 或 [IPv6]
        end = h.find(']')
        if end != -1:
            ipv6 = h[1:end]
            return ipv6  # 去掉端口和 []
        return h  # malformed fallback

    # 尝试解析为纯 IPv6（无端口）
    try:
        ip = ipaddress.ip_address(h)
        return str(ip)
    except ValueError:
        pass

    # 处理 host:port
    if ':' in h:
        # 只按最后一个 : 切（避免误伤 IPv6-like 字符串）
        host_part, port_part = h.rsplit(':', 1)
        # 如果 port 是数字，认为是端口
        if port_part.isdigit():
            return host_part

    return h

def _is_subdomain(host, domain):
    return host == domain or host.endswith("." + domain)


def is_host_allowed(host, whitelist=admin.qrcode_allow_hosts, allow_subdomains=admin.qrcode_allow_subdomains):
    #whitelist 示例：["example.com", "api.service.io", "192.168.1.1","2409::1"]
    norm = normalize_host(host)
    if not whitelist or whitelist == [''] or whitelist == ['*']:
        return True
    if not norm:
        return False
    for allowed in whitelist:
        allowed = allowed.lower()
        if norm == allowed:
            return True
        elif allow_subdomains:
            if _is_subdomain(norm, allowed):
                return True
    return False


if __name__ == '__main__':
    test_is62hex = ['4325','f3442','CD3432f','234_8342','dfsad-32','23F*B',4321543]
    for i in test_is62hex:
        print(i, is62hex(i))

    print(normalize_host('FE80::3'))
    print(normalize_host('[FE80::3]:93'))
    print(is_host_allowed('example.com'))
