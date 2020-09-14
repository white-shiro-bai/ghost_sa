# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)

from configs import admin
import requests
import traceback
from configs.export import write_to_log

def get_json_from_api(url):
    headers = {
        'User-agent': admin.who_am_i
    }
    try:
        req = requests.get(url=url,headers=headers)
        result = req.json()
        return result
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_api',result=error)

def get_json_from_postjson(url,data):
    headers = {
        'User-agent': admin.who_am_i
    }
    try:
        req = requests.post(url=url,headers=headers,json=data)
        result = req.json()
        return result
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_postjson',result=error)