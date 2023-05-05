# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2023-05-05 09:57:56
#FilePath: \ghost_sa_github_cgq\component\public_func.py
#
import sys
sys.path.append('./')
from guppy import hpy
import re

def show_my_memory():
    hxx = hpy()
    heap = hxx.heap()
    mem = re.search("Total size = (.*) bytes.",str(heap)).group(1)
    return mem

def key_counter(group={},keytype='',key=''):
    if keytype not in group:
        group[keytype]={}
    if key not in group[keytype]:
        group[keytype][key]=0
    group[keytype][key]+=1
    return group

if __name__ == '__main__':
    print(show_my_memory())