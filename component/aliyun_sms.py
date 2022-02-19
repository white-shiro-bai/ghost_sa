# -*- coding: utf-8 -*-
#
#Date: 2022-02-07 13:54:46
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-02-19 18:30:44
#FilePath: \ghost_sa_github\component\aliyun_sms.py
#

# this function reference from https://github.com/migege/aliyun-sms-api/


import sys
sys.path.append('./')
from configs import aliyun_sms_conf,admin
from configs.export import write_to_log
import traceback
from datetime import datetime
import uuid
import requests

def sendsms(phone_number, template_param, template_code, sign_name=aliyun_sms_conf.default_signname):
    url = aliyun_sms_conf.aliyun_sms_sent
    data = {
        'AccessKeyId': aliyun_sms_conf.accessKeyId,
        'Action': 'SendSms',
        'Format': 'JSON',
        'PhoneNumbers': phone_number,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid4()),
        'SignatureVersion': '1.0',
        'SignName': sign_name,
        'TemplateCode': template_code,
        'TemplateParam': template_param,
        'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'Version': '2017-05-25',
    }

    def __percent_encode(s):
        import urllib
        s = urllib.parse.quote(str(s), '').replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
        return s

    def __gen_signature(data, req_method):
        import hashlib
        import hmac
        import base64

        sorted_data = sorted(data, key=lambda v: v[0])
        vals = []
        for k, v in sorted_data:
            vals.append(__percent_encode(k) + '=' + __percent_encode(v))
        params = '&'.join(vals)
        string_to_sign = req_method + '&%2F&' + __percent_encode(params)
        key = aliyun_sms_conf.accessKeySecret + '&'
        step1 = hmac.new(bytes(key, encoding='utf-8'), bytes(string_to_sign,encoding='utf-8'), hashlib.sha1).digest().strip()
        signature = base64.encodestring(step1).decode('utf-8').replace('\n','')
        return signature

    try:
        headers = {
            'User-agent': admin.who_am_i,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        signature = __gen_signature(data.items(), 'POST')
        data['Signature'] = signature
        r = requests.post(url, data=data, headers=headers).json()
        print(r['Code'])
        if r['Code'] == 'OK' or r['Message'] == 'OK':
            return 'success'
        elif r['Code'] == 'isv.Customer_refused' or r['Message'] == '用户已退订推广短信':
            return 'junk'
        else:
            return str(r)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='aliyun_sms', defname='sendsms', result=error)
        return 'check_fail_log'


if __name__ == '__main__':
    sendsms(phone_number='15600000000', template_param="{'name': '142', 'date': '75天', 'sku': '专业版'}", template_code='SMS_200000000', sign_name='测试邮件')