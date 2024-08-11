# -*- coding: utf-8 -*-
#
#Date: 2023-05-28 17:11:16
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-06-29 12:18:49
#FilePath: \ghost_sa_github_cgq\configs\db.py
#
import sys
sys.path.append('./')
import pymysql
from configs import admin

# 数据库连接

def get_conn_sqldb():
    # 数据库连接程序，支持MySQL 5.7以上和TiDB3
    host = '192.168.193.23'  # 服务器地址
    port = 4000  # 端口号
    user = 'test'  # 用户名
    passwd = 'test'
    db = 'testbase'  # 库名
    if admin.database_type == 'tidb-serverless' :
        conn = pymysql.connect(host=host, port=port, user=user,passwd=passwd, db=db, charset='utf8mb4', client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,ssl_ca=admin.ca_local[admin.serverless_system])
        return conn
    conn = pymysql.connect(host=host, port=port, user=user,passwd=passwd, db=db, charset='utf8mb4', client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)
    return conn