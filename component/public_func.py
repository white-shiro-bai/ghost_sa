# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-01-13 19:30:26
#FilePath: \ghost_sa_github_cgq\component\public_func.py
#
import sys
sys.path.append('./')
from guppy import hpy
import re
from pympler import asizeof

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

if __name__ == '__main__':
    print(show_my_memory())