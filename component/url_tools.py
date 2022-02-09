# -*- coding: utf-8 -*-
#
#Date: 2021-09-18 16:29:59
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-02-09 10:42:23
#FilePath: \ghost_sa_github\component\url_tools.py
#
import sys
sys.path.append("./")
from flask import request
import urllib
from configs.export import write_to_log


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