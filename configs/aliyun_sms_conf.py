# -*- coding: utf-8 -*-
#
#Date: 2022-02-07 10:17:13
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-02-19 17:20:37
#FilePath: \ghost_sa_github\configs\aliyun_sms_conf.py
#
import sys
sys.path.append('./')

accessKeyId = 'accessKeyId' #参考文档 https://help.aliyun.com/document_detail/101339.html

accessKeySecret = 'accessKeySecret' #参考文档 https://help.aliyun.com/document_detail/101339.html

aliyun_sms_sent = 'https://dysmsapi.aliyuncs.com' #发送短信 参考文档 https://help.aliyun.com/document_detail/101511.html

aliyun_sms_recieve = 'https://dybaseapi.aliyuncs.com' #消息接收1 参考文档 https://help.aliyun.com/document_detail/101511.html

default_signname  = '注册验证' #缺省签名 当没有签名时，使用此签名