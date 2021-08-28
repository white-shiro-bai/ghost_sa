import requests
import os
import traceback
import time
from app.configs.export import write_to_log



# 神策官方程序的连接方法。用来导出神策历史数据进入鬼策
# 神策执行sql查询返回json


def exesqlsc(sql, retry=10):
    # 生产库
    project = "production"  #神策项目名
    token = "your_token_here"   #项目Token，在神策原生管理员账号下查看
    output_format = "json"   #返回数据格式
    base_url = "https://your_sensors_domain:8107/api/sql/query"  #神策页面的域名
    try:
        req = requests.post(url=base_url, params={
                            "project": project, "token": token, "q": sql, "format": output_format})
        result = req.text
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='sensorsSQL',defname='exesqlsc', result=sql+error)
        if retry > 0:
            retry -= 1
            time.sleep(1)
            return exesqlsc(sql=sql, retry=retry)
        else:
            result = error
    return result
