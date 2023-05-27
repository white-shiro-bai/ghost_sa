# -*- coding: utf-8 -*-
#
#Date: 2022-03-13 00:19:41
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2023-05-27 20:49:33
#FilePath: \ghost_sa_github_cgq\component\shorturl.py
#
import sys
sys.path.append('./')
from configs.export import write_to_log
from component.db_func import find_max_shortcut_dec,get_long_url_from_short
from component.base62 import Base62

def get_ghost_sa_short_url(max_add=1000):
    #find max dec number
    max_number = find_max_shortcut_dec()
    base62 = Base62()
    while max_add>0:
        short_url = base62.encode_10to62(max_number+1)
        short_url_status = get_long_url_from_short(short_url=short_url)[1]
        if short_url_status == 'fail':
            return short_url,'ok',max_number+1
        else:
            write_to_log(filename='shorturl',defname='get_ghost_sa_short_url',result=short_url+'存在重复，将自增一个继续尝试，当前dec='+str(max_number)+'剩余尝试次数'+str(max_add))
            max_number += 1
            max_add -= 1
    return '','fail',-2


if __name__ == "__main__":
    # get_suoim_short_url(long_url='')
    print(get_ghost_sa_short_url())
