# -*- coding: utf-8 -*-
#
#Date: 2023-05-27 21:19:00
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-14 14:31:03
#FilePath: \ghost_sa_github_cgq\selftest\test_case.py
#
import sys
sys.path.append('./')
from component.api_req import get_json_from_postjson
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED

def test_source_generate():
    # with open('./selftest/ipbase.txt','r',encoding='utf-8') as ipbase:
    #     ipbase_list = ipbase.readlines()
    #     for i in range(0,len(ipbase_list)):
    #         ipbase_list[i] = (i,ipbase_list[i].split('\t')[0],ipbase_list[i].split('\t')[1].strip('\n'))
    with open('./selftest/user_agent.txt','r',encoding='utf-8') as user_agent:
        useragent_list = user_agent.readlines()
        for j in range(0,len(useragent_list)):
            useragent_list[j] = (j,useragent_list[j].split('\t')[0],useragent_list[j].split('\t')[1].strip('\n'))
    return useragent_list


def test_shortcut(count=1000):
    for i in range(0,count) :
        with ThreadPoolExecutor(max_workers=50) as worker:
            worker.submit(req,id=i)
def req(id):
    result = get_json_from_postjson(url='http://localhost:8000/shortit',data={'org_url':'http://www.{count}.com'.format(count=id)})
    print(result)

def batch_send_deduplication():
    pass


if __name__ == '__main__':
    # test_shortcut(count=1000)
    print(test_source_generate())
