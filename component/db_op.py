# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2023-05-27 16:07:22
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

def exe_tidb(sql, args=None,presql=None):
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

def select_tidb(sql, args=None,presql=None):
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


def do_tidb_exe(sql,presql=None, args=None, retrycount=5):
    # 带保护执行库
    if  sql.lower().startswith('update') and "where" not in sql.lower():
        write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+'update必须包含where条件才能执行')
        return 'update必须包含where条件才能执行', 0 , 0
    elif  sql.lower().startswith('delete') and "where" not in sql.lower():
        write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+'delete必须包含where条件才能执行')
        return 'delete必须包含where条件才能执行', 0 , 0
    else:
        try:
            results, result_count , lastest_id = exe_tidb(sql=sql, args=args,presql=presql)
            return results, result_count , lastest_id
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='db_op', defname='do_tidb_exe', result=sql+str(args)+error)
            if retrycount > 0:
                retrycount -= 1
                time.sleep(1)
                return do_tidb_exe(sql=sql, args=args, retrycount=retrycount)
            else:
                return 'sql_err', 0 , 0


def do_tidb_select(sql,presql=None, args=None, retrycount=5):
    # 带保护查询库
    try:
        results, result_count = select_tidb(sql=sql, args=args,presql=presql)
        return results, result_count
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='db_op', defname='do_tidb_select', result=error)
        if retrycount > 0:
            retrycount -= 1
            time.sleep(1)
            return do_tidb_select(sql=sql, args=args, retrycount=retrycount)
        else:
            return 'sql_err', 0

if __name__ == "__main__":
    print(do_tidb_exe('show tables'))
