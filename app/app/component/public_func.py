# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from guppy import hpy
import re

def show_my_memory():
    hxx = hpy()
    heap = hxx.heap()
    mem = re.search("Total size = (.*) bytes.",str(heap)).group(1)
    return mem

if __name__ == '__main__':
    print(show_my_memory())