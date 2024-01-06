# -*- coding: utf-8 -*-
#
#Date: 2024-01-06 19:33:58
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-06 20:56:31
#FilePath: \ghost_sa_github_cgq\component\local_cache.py
#
import sys
sys.path.append('./')
from component.public_func import show_my_memory
from pympler import asizeof


class batch_send_deduplication():
    def __init__(self):
        self.cache={}
    
    def query(self,distinct_id,lib,track_id,time13):

        pass

    def traffic(self):
        pass
    

class test_memory():
    def __init__(self):
        self.data = {}
        self.data2 = {}
    
    def insert(self,max_cycle=1000):
        for i in range(max_cycle):
            self.data[i] ={}
            self.data2[i] ={}
            for j in range(100000):
                self.data[i][j] = """{"_track_id": 29601519, "distinct_id": "16d69282477336-0212e5ad1ba155-3c604504-2073600-16d6928247822b", "event": "$pageview", "extractor": {"c": 173518406, "e": "data.tvcbook.sa", "f": "(dev=fd11,ino=23599895)", "n": "access_log.2019092600", "o": 4637044, "s": 173518406}, "lib": {"$lib": "js", "$lib_method": "code", "$lib_version": "1.13.10"}, "map_id": "16d69282477336-0212e5ad1ba155-3c604504-2073600-16d6928247822b", "project": "production", "project_id": 2, "properties": {"$browser": "Chrome", "$browser_version": "63.0.3239.132", "$city": "德阳", "$country": "中国", "$ip": "171.211.123.58", "$is_first_day": true, "$is_first_time": true, "$is_login_id": false, "$latest_referrer": "", "$latest_referrer_host": "", "$latest_search_keyword": "未取到值_直接打开", "$latest_traffic_source_type": "直接流量", "$lib": "js", "$lib_version": "1.13.10", "$os": "Windows", "$os_version": "10", "$province": "四川", "$referrer": "", "$referrer_host": "", "$screen_height": 1080, "$screen_width": 1920, "$title": "TVCBOOK优视 - 广告视频搜索社交网络", "$url": "https://www.tvcbook.com/", "$url_path": "/", "owner": "SDKAuto"}, "recv_time": 1569427303537, "time": 1569427303537, "type": "track", "user_id": 7612250081099085201, "ver": 2}"""
                self.data2[i][j] = """{"_track_id": 29601519, "distinct_id": "16d69282477336-0212e5ad1ba155-3c604504-2073600-16d6928247822b", "event": "$pageview", "extractor": {"c": 173518406, "e": "data.tvcbook.sa", "f": "(dev=fd11,ino=23599895)", "n": "access_log.2019092600", "o": 4637044, "s": 173518406}, "lib": {"$lib": "js", "$lib_method": "code", "$lib_version": "1.13.10"}, "map_id": "16d69282477336-0212e5ad1ba155-3c604504-2073600-16d6928247822b", "project": "production", "project_id": 2, "recv_time": 1569427303537, "time": 1569427303537, "type": "track", "user_id": 7612250081099085201, "ver": 2}"""
            print(i,sys.getsizeof(self.data),sys.getsizeof(self.data2),asizeof.asizeof(self.data),asizeof.asizeof(self.data2),show_my_memory(),int(asizeof.asizeof(self.data))-int(asizeof.asizeof(self.data2)),int(show_my_memory())-int(asizeof.asizeof(self.data))-int(asizeof.asizeof(self.data2)))
    def delect(self):
        for i in range(len(self.data)):
            del self.data[i]
            print(i,sys.getsizeof(self.data),sys.getsizeof(self.data2),asizeof.asizeof(self.data),asizeof.asizeof(self.data2),show_my_memory(),int(asizeof.asizeof(self.data))-int(asizeof.asizeof(self.data2)),int(show_my_memory())-int(asizeof.asizeof(self.data))-int(asizeof.asizeof(self.data2)))
        print(self.data)

if __name__ == '__main__':
    obj = test_memory()
    obj.insert(max_cycle=10)
    obj.delect()
