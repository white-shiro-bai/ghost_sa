# -*- coding: utf-8 -*-
#
#Date: 2024-01-21 14:24:35
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-21 18:51:08
#FilePath: \ghost_sa_github_cgq\configs\redis_connect.py
#
import sys
sys.path.append('./')
import redis
from configs.export import write_to_log


def redis_db_conn(datebase_number=None):
    if datebase_number is None:
        write_to_log(filename='redis_connect.py',defname='redis_db_conn',result='datebase_number is undifined, connection fobbiden to pervent database abuse.')
        return None
    # pool = redis.ConnectionPool(host='ghost_sa', port=6379, decode_responses=True, password='admin',db=datebase_number)
    # redis_db = redis.Redis(connection_pool=pool)
    redis_db = redis.Redis(host='ghost_sa', port=6379, decode_responses=True, password='admin',db=datebase_number)
    return redis_db

if  __name__ == '__main__':
    import time
    redis_db_conn(datebase_number=1).set('test10s', 'd',ex = 1)
    redis_db_conn(datebase_number=1).set('test10s', 'e',ex = 10)
    for i in range(12):
        print (i,redis_db_conn(datebase_number=1).get('test10s'))
        time.sleep(1)