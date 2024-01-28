# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-28 18:32:30
#FilePath: \ghost_sa_github_cgq\component\db_op.py
#
import sys
sys.path.append('./')
# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from configs.export import write_to_log
import traceback
import time
from configs.db import *

# 数据库操作

def _exe_tidb(sql, args=None,presql=None):
    #连接器中间层
    #执行数据库操作
    conn = get_conn_sqldb()
    cur = conn.cursor()
    if presql:
        cur.execute(query=presql)
    result_count = cur.execute(query=sql, args=args)
    results = cur.fetchall()
    conn.commit()
    lastest_id_count = cur.execute(query="""SELECT LAST_INSERT_ID();""")
    lastest_id = cur.fetchone()
    cur.close()
    conn.close()
    return results, result_count, lastest_id[0]

def _select_tidb(sql, args=None,presql=None):
    #连接器中间层
    #数据库只读操作
    conn = get_conn_sqldb()
    cur = conn.cursor()
    if presql:
        cur.execute(query=presql)
    result_count = cur.execute(query=sql, args=args)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results, result_count


def do_tidb_exe(sql,presql=None, args=None, retrycount=5,skip_mysql_code = 0):
    # 带保护执行库
    if  sql.lower().startswith('update') and "where" not in sql.lower():
        write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+'update必须包含where条件才能执行')
        return 'update必须包含where条件才能执行', 0 , 0
    elif  sql.lower().startswith('delete') and "where" not in sql.lower():
        write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+'delete必须包含where条件才能执行')
        return 'delete必须包含where条件才能执行', 0 , 0
    else:
        while retrycount >= 0:
            try:
                results, result_count , lastest_id = _exe_tidb(sql=sql, args=args,presql=presql)
                return results, result_count , lastest_id
            except Exception:
                error = traceback.format_exc()
                if sys.exc_info()[1].args[0] != skip_mysql_code :
                    write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+error)
                retrycount -= 1
                time.sleep(1)
                    # return do_tidb_exe(sql=sql, args=args, retrycount=retrycount)
        return 'sql_err', 0 , 0 #只在日志里记录错误，不返回错误，避免引用的时候不小心泄露代码。


def do_tidb_select(sql,presql=None, args=None, retrycount=5):
    # 带保护查询库
    while retrycount >= 0:
        try:
            results, result_count = _select_tidb(sql=sql, args=args,presql=presql)
            return results, result_count
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='db_op', defname='do_tidb_select', result=error)
            retrycount -= 1
            time.sleep(1)
        return 'sql_err', 0 #只在日志里记录错误，不返回错误，避免引用的时候不小心泄露代码。

if __name__ == "__main__":
    # print(do_tidb_exe('show tables'))
    from component.public_value import get_time_str,current_timestamp
    sql = 'insert into `deduplication_key` (`project`,`distinct_id`,`track_id`,`sdk_time13`,`created_at`) values ( %(project)s,%(distinct_id)s,%(track_id)s,%(sdk_time13)s,%(created_at)s)'
    key = {'project': 'test_me', 'distinct_id': 'test123', 'track_id': '4567', 'sdk_time13':1234567890123 ,'created_at':get_time_str(inttime=current_timestamp10())}
    print(do_tidb_exe(sql=sql, args=key,retrycount=0,skip_mysql_code=1062))