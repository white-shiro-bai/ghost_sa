# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-07-13 20:06:14
#FilePath: \ghost_sa_github_cgq\component\we_chat.py
#
import sys
sys.path.append('./')
import json
from configs.export import write_to_log
from component.api_req import get_json_from_api,get_json_from_postjson
from configs import wechat
import traceback

def getWeChatToken():
    appid = wechat.AppID  # 微信公众号开发者ID(AppID)
    secret = wechat.AppSecret  # 微信公众号开发者密码(AppSecret)
    # 获取access_token和日期
    accessTokenURL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret 
    return get_json_from_api(accessTokenURL)['access_token']

def post_wechat_notification(data):
    post_data_json = {
           "touser":data['wechat_openid'],
           "template_id":data['wechat_template_id'],
           "data":data['data']}
    if    'target_url' in data:
        post_data_json['url'] = data['target_url']
    if "miniprogram" in data:
        post_data_json['miniprogram'] =  {
             "appid": data['miniprogram_id'],"pagepath":data['miniprogram_pagepath']}
    try:
        result = get_json_from_postjson(url='https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='+getWeChatToken(),data=post_data_json)
        if result['errcode'] == 0:
            return 'success'
        else:
            return str(result)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='wechat', defname='post_wechat_notification', result=error)
        return 'check_fail_log'
