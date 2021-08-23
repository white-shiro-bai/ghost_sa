# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from flask import request
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)


def get_url_params(params):
    #获取参数信息，JSON》FORM》ARGS的顺序
    try:
        got_json = request.json
    except:
        got_json = None
    v = None
    if got_json:
        if params in got_json:
            v = got_json[params]
    elif v == '' or not v:
        if request.method == 'POST':
            v = request.form.get(params)
        elif request.method == 'GET':
            v = request.args.get(params)
        elif request.method == 'POST' and not v:
            v = request.args.get(params)
        elif request.method == 'GET' and not v:
            v = request.form.get(params)
    if v and v != '':
        return v
    else:
        return None

def get_ip():
    if request.headers.get('X-Forwarded-For') is None:
        ip = request.remote_addr#服务器直接暴露
    else:
        ip = request.headers.get('X-Forwarded-For') #获取SLB真实地址
    return ip