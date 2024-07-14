# -*- coding: utf-8 -*-
#
#Date: 2023-05-28 17:13:42
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-04-14 15:45:34
#FilePath: \ghost_sa_github_cgq\configs\export.py
#
import sys
sys.path.append('./')
import csv
import codecs
import datetime
import os


def write_to_log(filename, defname, result,level='info'):
    #level包含info，debug，warning，error
    # 输出日志，filename是.py的的名字，def是方法名，result是要记录的内容
    dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
    dirpath = os.path.join('log', dirdate)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, filename+'.log')
    tofile = open(filepath, mode='a+', encoding='utf-8')
    content = str(datetime.datetime.now()) + ',' + defname + ',' + result
    print(content, file=tofile)
    print(content)
