# -*- coding: utf-8 -*-
#
#Date: 2023-05-27 21:19:00
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2023-05-27 21:40:22
#FilePath: \ghost_sa_github_cgq\tools\test_case.py
#
import sys
sys.path.append('./')
from component.api_req import get_json_from_postjson
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED


def test_shortcut(count=1000):
    for i in range(0,count) :
        with ThreadPoolExecutor(max_workers=50) as worker:
            worker.submit(req,id=i)
def req(id):
    result = get_json_from_postjson(url='http://localhost:8000/shortit',data={'org_url':'http://www.{count}.com'.format(count=id)})
    print(result)


if __name__ == '__main__':
    test_shortcut(count=1000)
