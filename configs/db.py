# -*- coding: utf-8 -*-
#
#Date: 2023-05-28 17:11:16
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2025-06-08 22:21:01
#FilePath: \ghost_sa_github_cgq\configs\db.py
#
import sys
sys.path.append('./')
from configs import admin
from mysql.connector.constants import ClientFlag
from mysql.connector import pooling

# 数据库配置
ghost_sa_db_config = {
    'host': '192.168.193.23',
    'port': 4000,
    'user': 'test',
    'password': 'test',
    'database': 'testbase',
    'charset': 'utf8mb4',
    'client_flags': [ClientFlag.MULTI_STATEMENTS]
}
if admin.database_type == 'tidb-serverless' :
    ghost_sa_db_config['ssl_ca'] = admin.ca_local[admin.serverless_system]
    ghost_sa_db_config['ssl_verify_cert'] = True
    ghost_sa_db_config['sslmode'] = 'VERIFY_CA'

# 创建数据库连接池

ghost_sa_connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=20,  # 设置连接池大小
    **ghost_sa_db_config
)

def get_conn_sqldb():
    #从连接池中获取一个数据库连接
    return ghost_sa_connection_pool.get_connection()