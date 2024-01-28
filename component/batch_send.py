# -*- coding: utf-8 -*-
#
#Date: 2024-01-06 19:33:58
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-28 18:57:37
#FilePath: \ghost_sa_github_cgq\component\batch_send.py
#
import sys
sys.path.append('./')
from component.public_func import show_obj_size
from component.db_func import insert_deduplication_key,delete_deduplication_key,count_deduplication_key
from component.public_value import current_timestamp10,get_time_str
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

        if self.batch_send_deduplication_mode in ('redis'):
            from configs.redis_connect import redis_db_conn
            self.batch_redis_conn = redis_db_conn(datebase_number=admin.batch_send_redis_db_number)
            write_to_log(filename='batch_send',defname='init',result='完成使用redis去重初始化')
        elif self.batch_send_deduplication_mode in ('none'):
            write_to_log(filename='batch_send',defname='init',result='未开启去重功能')
        elif self.batch_send_deduplication_mode in ('ram'):
            write_to_log(filename='batch_send',defname='init',result='使用ram去重初始化完成')
        elif self.batch_send_deduplication_mode in ('consumer'):
            write_to_log(filename='batch_send',defname='init',result='消费者去重模式初始化完成')
        elif self.batch_send_deduplication_mode in ('tidb6.5+','tidb6.4-','mysql','mysql-memory'):
            write_to_log(filename='batch_send',defname='init',result='使用数据库去重初始化完成')

    def query(self,project='',distinct_id='',track_id=0,time13=0,source='api'):
        if (source == 'api' and self.batch_send_deduplication_mode == 'consumer') or self.batch_send_deduplication_mode == 'none' :
            return 'go'
        else :
            if not track_id or track_id  == 0 or track_id  =='0' or not time13 or time13 == 0:
                return 'go'
            elif track_id and track_id !=0 and track_id != '0' and time13 and time13 !=0:
                batch_key = project + distinct_id
                trackey = str(track_id) + str(time13)
                combinekey=batch_key+trackey
                # write_to_log(filename='batch_send',defname='query',result='batch_key:'+batch_key+',trackey:'+trackey)
                if self.batch_send_deduplication_mode in ('ram','consumer'):
                    res = self._ram_query(batch_key=batch_key,trackey=trackey,time13=time13)
                    if res :
                        # write_to_log(filename='batch_send',defname='query',result='skip:'+'batch_key:'+batch_key+',trackey:'+trackey+' ,'+str(res))
                        return 'skip'
                # elif self.batch_send_deduplication_mode == 'redis':
                elif self.batch_send_deduplication_mode in ('redis'):
                    res = self._redis_query(combinekey=combinekey,time13=time13)
                    if res :
                        return 'skip'
                elif self.batch_send_deduplication_mode in ('tidb6.5+','tidb6.4-','mysql','mysql-memory'):
                    res = self._db_query(project=project,distinct_id=distinct_id,track_id=track_id,time13=time13)
                    if res :
                        return 'skip'
                else:
                    write_to_log(filename='batch_send',defname='query',result='query not support mode')
                self._insert(batch_key=batch_key,trackey=trackey,time13=time13)
                # write_to_log(filename='batch_send',defname='query',result='go:'+batch_key+','+trackey )
                return 'go'

    def _insert(self,batch_key,trackey,time13):
        if self.batch_send_deduplication_mode in ('ram','consumer'):
            self._ram_insert(batch_key=batch_key,trackey=trackey,time13=time13)
        elif self.batch_send_deduplication_mode =='redis':
            pass
        elif self.batch_send_deduplication_mode in ('tidb6.5+','tidb6.4-','mysql','mysql-memory'):
            pass
        else:
            write_to_log(filename='batch_send',defname='_insert',result='insert not support mode')

    def clean_expired(self):
        if self.batch_send_deduplication_mode in ('ram','consumer'):
            self._ram_clean()
        elif self.batch_send_deduplication_mode in ('tidb6.4-'):
            self._db_clean()

    def _ram_insert(self,batch_key,trackey,time13):
        if batch_key in self.cache.keys():
            self.cache[batch_key]['track_ids'].append(trackey)
            if time13 >= self.cache[batch_key]['time13']:
                self.cache[batch_key]['time13'] = time13
        else:
            self.cache[batch_key] = {}
            self.cache[batch_key]['track_ids'] = [trackey]
            self.cache[batch_key]['time13'] = time13

    def _ram_query(self,batch_key,trackey,time13):
        req = None
        if batch_key in self.cache.keys() and trackey in self.cache[batch_key]['track_ids']:
            req = True
        return req

    def _redis_query(self,combinekey,time13):
        res = self.batch_redis_conn.set(name=combinekey, value=time13, ex=self.batch_send_max_window*60 , nx= True)
        if res == True:
            return None
        return 'key in redis'

    def _db_query(self,project,distinct_id,track_id,time13):
        if insert_deduplication_key(project=project,distinct_id=distinct_id,track_id=track_id,sdk_time13=time13) == 1:
            return None
        return 'key in db'

    def _ram_clean(self):
        keys_count = len(self.cache.keys())
        cache_size = show_obj_size(self.cache)
        cache_status = 'cache size:' + str(cache_size) + \
            '; batch_send_max_memory_limit:' + str(self.batch_send_max_memory_limit) + \
            '; keys count:'+ str(keys_count) + \
            '; keys limit:'+ str(self.batch_send_max_batch_key_limit) + \
            '; expired window:'+ str(self.batch_send_max_window*60*1000)
        write_to_log(filename='batch_send',defname='_ram_clean',result=cache_status)

        if cache_size >= self.batch_send_max_memory_limit or keys_count >= self.batch_send_max_batch_key_limit:
            write_to_log(filename='batch_send',defname='_ram_clean',result='exec_clean start')
            timenow13 = int(round(time.time() * 1000))
            for key in list(self.cache.keys()):
                if self.cache[key]['time13'] + (self.batch_send_max_window*60*1000) < timenow13:
                    del self.cache[key]
            cache_size_after_clean = show_obj_size(self.cache)
            write_to_log(filename='batch_send',defname='_ram_clean',result='cache size after clean:'+str(cache_size_after_clean))
            print(self.cache)
            if cache_size_after_clean >= self.batch_send_max_memory_limit:
                self.cache = {}
                write_to_log(filename='batch_send',defname='_ram_clean',result='!warning cache size after clean is still too large,clean all. please scale up batch_send_max_memory_limit or scale down expired window.')

    def _db_clean(self):
        beforeclean_size = count_deduplication_key()
        delete_deduplication_key(expired_time=get_time_str(inttime=current_timestamp10()-admin.batch_send_max_window*60))
        afterclean_size = count_deduplication_key()
        write_to_log(filename='batch_send',defname='_db_clean',result='duplication_key before clean:'+str(beforeclean_size)+', after clean:'+str(afterclean_size))


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