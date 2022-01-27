# -*- coding: utf-8 -*-
#
#Date: 2022-01-25 15:12:30
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2022-01-27 14:59:18
#FilePath: \ghost_sa_github\configs\umail.py
#
import sys
sys.path.append('./')

umail_host = "smtp.bestedm.org"
umail_port = 2525 # umail recommend use port 2525 instead of port 25 which is banned by aliyun.
umail_user = "联系umail开通"
umail_pass = "联系umail开通"
web_username = 'umail的账号'
web_password = 'umail的密码'
default_project = 'test_me' #default project name. Function component/umail.py will get failed email list everyday and insert them into recall_blacklist. As the reason of project is not required for umail, it has to privide a default project for all bad email reciever.