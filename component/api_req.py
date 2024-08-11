# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-07-13 20:07:16
#FilePath: \ghost_sa_github_cgq\component\api_req.py
#
import sys
sys.path.append('./')
from configs import admin
import requests
import traceback
from configs.export import write_to_log

def get_json_from_api(url,ua=admin.who_am_i):
    headers = {
        'User-agent': ua
    }
    try:
        req = requests.get(url=url,headers=headers)
        result = req.json()
        return result
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_api',result=error)

def get_json_from_postjson(url,data,ua=admin.who_am_i):
    headers = {
        'User-agent': ua
    }
    try:
        req = requests.post(url=url,headers=headers,json=data)
        result = req.json()
        return result
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_postjson',result=error)

def get_anyting_from_postjson(url,data,ua=admin.who_am_i):
    headers = {
        'User-agent': ua
    }
    try:
        req = requests.post(url=url,headers=headers,json=data)
        return req
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_postjson',result=error)

def get_anyting_from_get(url,ua=admin.who_am_i):
    headers = {
        'User-agent': ua
    }
    try:
        req = requests.get(url=url,headers=headers)
        return req
    except Exception:
      error = traceback.format_exc()
      write_to_log(filename='api_req',defname='get_json_from_api',result=error)