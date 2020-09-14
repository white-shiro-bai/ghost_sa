# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
print(sys.path)
from configs.weibo import *
from configs.suoim import *
import requests
from configs.export import write_to_log

def get_weibo_short_url(long_url):
    req = requests.get(url=weibo_shorten_url,params='source='+weibo_app_key+'&url_long='+long_url)
    # req = requests.get(url=weibo_shorten_url,params='access_token='+'36c70ad1f5238d7b55e1c99d51563123'+'&url_long='+long_url)
    try:
        result = req.json()
        print(result)
    except:
        #无法正常返回
        result = str(req)
        print(result)

def get_suoim_short_url(long_url):
    req = requests.get(url=suoim_shorten_url,params={'key':suoim_key,'format':'json','url':long_url})
    result = req.json()
    # print(type(result['err']))
    if result['err'] is None or result['err'] == '':
        short_url = result['url']
        return short_url,'ok'
        # print(short_url)
    else:
        # print(result['err'])
        return '','fail'
        write_to_log(filename='shorturl',defname='get_suoim_short_url',result=result['err'])


if __name__ == "__main__":
        get_suoim_short_url(long_url='')
