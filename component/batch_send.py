# -*- coding: utf-8 -*-
#
#Date: 2024-01-06 19:33:58
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-28 14:02:06
#FilePath: \ghost_sa_github_cgq\component\batch_send.py
#
import sys
sys.path.append('./')
from component.public_func import show_obj_size
from configs import admin
import time
from configs.export import write_to_log


class batch_send_deduplication():
    def __init__(self,batch_send_deduplication_mode=admin.batch_send_deduplication_mode,batch_send_max_memory_limit=admin.batch_send_max_memory_limit,batch_send_max_batch_key_limit=admin.batch_send_max_batch_key_limit,batch_send_max_memory_gap=admin.batch_send_max_memory_gap,batch_send_max_window=admin.batch_send_max_window):
        self.cache = {}
        #支持替换参数，便于单元测试
        self.batch_send_deduplication_mode=batch_send_deduplication_mode
        self.batch_send_max_memory_limit=batch_send_max_memory_limit
        self.batch_send_max_batch_key_limit=batch_send_max_batch_key_limit
        self.batch_send_max_memory_gap=batch_send_max_memory_gap
        self.batch_send_max_window=batch_send_max_window

        if self.batch_send_deduplication_mode in ('redis','consumer'):
            from configs.redis_connect import redis_db_conn
            self.batch_redis_conn = redis_db_conn(datebase_number=admin.batch_send_redis_db_number)
        print('batch_send初始化结束')
    
    def query(self,project='',distinct_id='',track_id=0,time13=0,source='api'):
        self.project = project
        self.distinct_id = distinct_id
        self.track_id = track_id
        self.time13 = time13
        print(self.project,self.distinct_id,self.track_id,self.time13,len(self.cache.keys()))
        if (source == 'api' and self.batch_send_deduplication_mode == 'consumer') or self.batch_send_deduplication_mode == 'none' :
            return 'go'
        else :
            if not self.track_id or self.track_id  == 0 or self.track_id  =='0' or not self.time13 or self.time13 == 0:
                return 'go'
            elif self.track_id and self.track_id !=0 and self.track_id != '0' and self.time13 and self.time13 !=0:
                self.batch_key = self.project + self.distinct_id
                self.trackey = str(self.track_id) + str(self.time13)
                write_to_log(filename='batch_send',defname='query',result='batch_key:'+self.batch_key+',trackey:'+self.trackey)
                if self.batch_send_deduplication_mode in ('ram','consumer'):
                    res = self._ram_query()
                    if res :
                        write_to_log(filename='batch_send',defname='query',result='skip:'+'batch_key:'+self.batch_key+',trackey:'+self.trackey+' ,'+str(res))
                        return 'skip'
                # elif self.batch_send_deduplication_mode == 'redis':
                elif self.batch_send_deduplication_mode in ('redis'):
                    res = self._redis_query()
                    if  res :
                        return 'skip'
                else:
                    write_to_log(filename='batch_send',defname='query',result='query not support mode')
                self._insert()
                write_to_log(filename='batch_send',defname='query',result='go:'+self.batch_key+','+self.trackey )
                return 'go'

    def _insert(self):
        if self.batch_send_deduplication_mode =='ram':
            self._ram_insert()
        elif self.batch_send_deduplication_mode =='redis':
            pass
        elif self.batch_send_deduplication_mode =='consumer':
            self._ram_insert()
        else:
            write_to_log(filename='batch_send',defname='query',result='insert not support mode')

    def clean_expired(self):
        if self.batch_send_deduplication_mode in ('ram','consumer'):
            self._ram_clean()

    def _ram_insert(self):
        if self.batch_key in self.cache.keys():
            self.cache[self.batch_key]['track_ids'].append(self.trackey)
            if self.time13 >= self.cache[self.batch_key]['time13']:
                self.cache[self.batch_key]['time13'] = self.time13
        else:
            self.cache[self.batch_key] = {}
            self.cache[self.batch_key]['track_ids'] = [self.trackey]
            self.cache[self.batch_key]['time13'] = self.time13

    def _ram_query(self):
        return self.batch_key in self.cache.keys() and self.trackey in self.cache[self.batch_key]['track_ids']

    def _redis_insert(self):
        self.batch_redis_conn.set(name=self.batch_key+self.trackey, value=self.time13, ex=self.batch_send_max_window*60)
        # self.batch_redis_conn.sadd(self.batch_key, self.trackey)
    def _redis_query(self):
        res = self.batch_redis_conn.set(name=self.batch_key+self.trackey, value=self.time13, ex=self.batch_send_max_window*60 , nx= True)
        if res == True:
            return None
        return 'skip'
        # if res == '1':
        #     return 'go'
        # else:
        #     return None
        # res = self.batch_redis_conn.sismember(self.batch_key, self.trackey)
        # return res

    def _ram_clean(self):
        keys_count = len(self.cache.keys())
        cache_size = show_obj_size(self.cache)
        cache_status = 'cache size:' + str(cache_size) + \
            '; batch_send_max_memory_limit:' + str(self.batch_send_max_memory_limit) + \
            '; keys count:'+ str(keys_count) + \
            '; keys limit:'+ str(self.batch_send_max_batch_key_limit) + \
            '; expired window:'+ str(self.batch_send_max_window*60*1000)
        write_to_log(filename='batch_send',defname='batch_send_deduplication',result=cache_status)

        if cache_size >= self.batch_send_max_memory_limit or keys_count >= self.batch_send_max_batch_key_limit:
            write_to_log(filename='batch_send',defname='batch_send_deduplication',result='exec_clean')
            timenow13 = int(round(time.time() * 1000))
            for key in list(self.cache.keys()):
                if self.cache[key]['time13'] + (self.batch_send_max_window*60*1000) < timenow13:
                    del self.cache[key]
            cache_size_after_clean = show_obj_size(self.cache)
            write_to_log(filename='batch_send',defname='batch_send_deduplication',result='cache size after clean:'+str(cache_size_after_clean))
            print(self.cache)
            if cache_size_after_clean >= self.batch_send_max_memory_limit:
                self.cache = {}
                write_to_log(filename='batch_send',defname='batch_send_deduplication',result='!warning cache size after clean is still too large,clean all. please scale up batch_send_max_memory_limit or scale down expired window.')


batch_cache = batch_send_deduplication()



if __name__ == '__main__':
    obj = batch_send_deduplication(batch_send_deduplication_mode='none',batch_send_max_memory_limit=100,batch_send_max_batch_key_limit=10,batch_send_max_memory_gap=10,batch_send_max_window=1)
    
    for i in range(500):
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