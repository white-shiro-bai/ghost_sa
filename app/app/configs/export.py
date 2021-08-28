import csv
import codecs
import datetime
import os


def write_to_log(filename, defname, result):
    # 输出日志，filename是.py的的名字，def是方法名，result是要记录的内容
    dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
    dirpath = os.path.join('log', dirdate)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, filename+'.log')
    tofile = open(filepath, mode='a+', encoding='utf-8')
    content = str(datetime.datetime.now()) + ',' + defname + ',' + result
    print(content, file=tofile)
    print(content)
