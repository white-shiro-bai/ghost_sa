# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-06-30 20:29:52
#FilePath: \ghost_sa_github_cgq\component\public_func.py
#
import sys
sys.path.append('./')
from guppy import hpy
import re
from pympler import asizeof
import time
import json
import gzip
import urllib.parse
import base64
from concurrent.futures import ThreadPoolExecutor
import queue


class multi_thread_pool(ThreadPoolExecutor):
    def __init__(self,max_workers=None, thread_name_prefix=''):
        super(multi_thread_pool,self).__init__(max_workers,thread_name_prefix)
        self._work_queue = queue.Queue(maxsize = max_workers)

def show_my_memory():
    #获取整个程序的内存占用，单位byte
    hxx = hpy()
    heap = hxx.heap()
    mem = re.search("Total size = (.*) bytes.",str(heap)).group(1)
    return mem

def show_obj_size(obj):
    #获取对象的内存占用，单位byte
    return int(asizeof.asizeof(obj))

def key_counter(group={},keytype='',key=''):
    if keytype not in group:
        group[keytype]={}
    if key not in group[keytype]:
        group[keytype][key]=0
    group[keytype][key]+=1
    return group

def data_generate(distinct_id='test_distinct_id',track_id=0,lib='js',time13=int(time.time()*1000),other_properties={},other_value={},copy='0'):
    #生成模拟数据，用来进行压力测试。
    data_json = {"_track_id": track_id, "anonymous_id": "1645844717318-3513716-0fabf7952c6188-54770152", "distinct_id": distinct_id, "event": "$MPShow", "lib": {"$lib": lib, "$lib_method": "code", "$lib_version": "1.14.19"}, "properties": {"$app_id": "wx2c2f802113293ce7", "$brand": "OPPO", "$is_first_day": "true", "$latest_scene": "wx-1035"+copy, "$lib": lib, "$lib_version": "1.14.19", "$manufacturer": "OPPO"+copy, "$model": "PCKM00"+copy, "$network_type": "WIFI", "$os": "Android", "$os_version": "11", "$referrer": "直接打开", "$referrer_title": "测试页面", "$scene": "wx-1035", "$screen_height": 756, "$screen_width": 360, "$timezone_offset": -480, "$url_path": "pages/eventList/index", "$url_query": "pages/eventList/index","utm_source":"✨☀👉","lastest_utm_medium":"👉✨☀"}, "time": time13, "type": "track"}
    data_json["properties"].update(other_properties)
    data_json.update(other_value)
    datazip= urllib.parse.quote(base64.b64encode((gzip.compress(json.dumps(data_json).encode('utf-8')))))
    dataszip = urllib.parse.quote(base64.b64encode((gzip.compress(json.dumps([data_json]).encode('utf-8')))))
    data= urllib.parse.quote(base64.b64encode((json.dumps(data_json).encode('utf-8'))))
    datas = urllib.parse.quote(base64.b64encode((json.dumps([data_json]).encode('utf-8'))))
    return {'data':data,'datazip':datazip,'datas':datas,'dataszip':dataszip,'data_json':data_json}

if __name__ == '__main__':
    # print(show_my_memory())
    print(data_generate())