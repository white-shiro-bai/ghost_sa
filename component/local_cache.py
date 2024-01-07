# -*- coding: utf-8 -*-
#
#Date: 2024-01-06 19:33:58
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-07 22:33:18
#FilePath: \ghost_sa_github_cgq\component\local_cache.py
#
import sys
sys.path.append('./')
from component.public_func import show_obj_size
from configs import admin
import time


class batch_send_deduplication():
    def __init__(self,batch_send_deduplication=admin.batch_send_deduplication,batch_send_max_memory_limit=admin.batch_send_max_memory_limit,batch_send_max_batch_key_limit=admin.batch_send_max_batch_key_limit,batch_send_max_memory_gap=admin.batch_send_max_memory_gap,batch_send_max_window=admin.batch_send_max_window):
        self.cache={}
        #支持替换参数，便于单元测试
        self.batch_send_deduplication=batch_send_deduplication
        self.batch_send_max_memory_limit=batch_send_max_memory_limit
        self.batch_send_max_batch_key_limit=batch_send_max_batch_key_limit
        self.batch_send_max_memory_gap=batch_send_max_memory_gap
        self.batch_send_max_window=batch_send_max_window
    
    def query(self,project='',distinct_id='',track_id=0,time13=0):
        print(self.cache)
        if self.batch_send_deduplication is False :
            return 'go'
        else :
            if not track_id or track_id == 0 or track_id =='0' or not time13 or time13 == 0:
                return 'go'
            elif track_id and track_id !=0 and track_id != '0' and time13 and time13 !=0:
                batch_key = project + distinct_id
                trackey = str(track_id) + str(time13)
                if batch_key in self.cache.keys() and trackey in self.cache[batch_key]['track_ids'] :
                    return 'skip'
                else:
                    self.insert(batch_key=batch_key,trackey=trackey,time13=time13)
                    return 'go'

    def insert(self,batch_key,trackey,time13):
        if batch_key in self.cache.keys():
            self.cache[batch_key]['track_ids'].append(trackey)
            if time13 >= self.cache[batch_key]['time13']:
                self.cache[batch_key]['time13'] = time13
        else:
            self.cache[batch_key] = {}
            self.cache[batch_key]['track_ids'] = [trackey]
            self.cache[batch_key]['time13'] = time13

    def clean_expired(self):
        print('cache size:',show_obj_size(self.cache))
        print('batch_send_max_memory_limit:',self.batch_send_max_memory_limit )
        print('keys count:',len(self.cache.keys()))
        print('keys limit:',self.batch_send_max_batch_key_limit)
        print('expired window:',self.batch_send_max_window*60*1000)
        if show_obj_size(self.cache) >= self.batch_send_max_memory_limit or len(self.cache.keys()) >= self.batch_send_max_batch_key_limit:
            timenow13 = int(round(time.time() * 1000))
            for key in list(self.cache.keys()):
                if self.cache[key]['time13'] + (self.batch_send_max_window*60*1000) < timenow13:
                    del self.cache[key]


if __name__ == '__main__':
    obj = batch_send_deduplication(batch_send_deduplication=True,batch_send_max_memory_limit=100,batch_send_max_batch_key_limit=10,batch_send_max_memory_gap=10,batch_send_max_window=0.1)
    
    for i in range(50):
        if i%2 == 0:
            distinct_id = str(i+1)
            track_id = i+1
        elif i%3 == 0:
            distinct_id = str(i)
            track_id = i
        else:
            distinct_id = str(i)
            track_id = i+1
        print(i,distinct_id,track_id,obj.query(project = 'test_me',distinct_id=distinct_id,track_id=track_id,time13=int(round(time.time()) * 1000)))
    for i in range(10):
        if i%2 == 0:
            distinct_id = str(i+1)
            track_id = i+1
        elif i%3 == 0:
            distinct_id = str(i)
            track_id = i
        else:
            distinct_id = str(i)
            track_id = i+1
        print(i,distinct_id,track_id,obj.query(project = 'test_me',distinct_id=distinct_id,track_id=track_id,time13=int(round(time.time()) * 1000)))
    obj.clean_expired()
    time.sleep(10)
    obj.clean_expired()
    for i in range(10):
        if i%2 == 0:
            distinct_id = str(i+1)
            track_id = i+1
        elif i%3 == 0:
            distinct_id = str(i)
            track_id = i
        else:
            distinct_id = str(i)
            track_id = i+1
        print(i,distinct_id,track_id,obj.query(project = 'test_me',distinct_id=distinct_id,track_id=track_id,time13=int(round(time.time()) * 1000)))