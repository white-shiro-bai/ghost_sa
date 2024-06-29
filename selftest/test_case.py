# -*- coding: utf-8 -*-
#
#Date: 2023-05-27 21:19:00
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2024-06-29 19:36:28
#FilePath: \ghost_sa_github_cgq\selftest\test_case.py
#
import sys
sys.path.append('./')
from component.api_req import get_json_from_postjson,get_anyting_from_get,get_anyting_from_postjson
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from component.public_func import data_generate
import time
from configs import admin
from configs.export import write_to_log
import random
from component.db_op import do_tidb_select

def test_ip_generate():
    with open('./selftest/ipbase.txt','r',encoding='utf-8') as ipbase:
        ipbase_list = ipbase.readlines()
        for i in range(0,len(ipbase_list)):
            ipbase_list[i] = (i,ipbase_list[i].split('\t')[0],ipbase_list[i].split('\t')[1].strip('\n'))
    return ipbase_list

def test_useragent_generate():
    with open('./selftest/user_agent.txt','r',encoding='utf-8') as user_agent:
        useragent_list = user_agent.readlines()
        for j in range(0,len(useragent_list)):
            useragent_list[j] = (j,useragent_list[j].split('\t')[0],useragent_list[j].split('\t')[1].strip('\n'))
    return useragent_list

def batch_send_deduplication(project='test_me',url='http://127.0.0.1:5000/' ,remark = 'normal' ,no_bot = ''):
#[root@ghost_sa ghost_test]# python3 selftest/test_case.py test19
# batch_send_deduplication执行完毕，用时： 33194
# 应收到请求数据: 2773 ,如开启去重，应包含正常数据: 1040 ,应包含特殊规则数据: 867 ,如果开启去重，实际去重数量应为: 866 ,如果未开启去重，插入数据应为 1906
# (('test21', '"track_id一致，上报时间戳不一致，多次重复都应该保留"', 867), ('test21', '"正常重复数据，重复写入只记1条"', 1906)) <-- 未开启去重且允许爬虫
# (('test16', '"track_id一致，上报时间戳不一致，多次重复都应该保留"', 867), ('test16', '"正常重复数据，重复写入只记1条"', 1040)) <-- 开启去重写允许爬虫
# (('test20', '"track_id一致，上报时间戳不一致，多次重复都应该保留"', 842), ('test20', 正常重复数据，重复写入只记1条"', 1015)) <-- 开启去重且不允许爬虫

    ipbase_list = test_ip_generate()
    useragent_list = test_useragent_generate()
    send_count = 0 # 实际发送条数，如果不开去重，应该与这个一致
    send_duplicate_count = 0 # 发送的重复数据，如果不开去重，应该有这些重复量
    send_recount_count = 0 # 发送的重复数据但不同时间戳，不应该被过滤
    indepent_count = 0 #准备的数据条数
    time_start = int(time.time()*1000)
    send_mode = ['post','get']
    send_zip = ['yes','no']
    with ThreadPoolExecutor(max_workers=50) as worker:
        for j in range(0,len(useragent_list)):
            indepent_count += 1
            j_count = 0
            time13 = int(time.time()*1000)
            j_rule_count = -1
            # time.sleep(0.0002)
            for i in range(1,4):
                if (j+1)%i == 0:
                    j_count += 1
                    send_count += 1
                    j_rule_count += 1
                    random.shuffle(ipbase_list)
                    random.shuffle(send_mode)
                    random.shuffle(send_zip)
                    ip = ipbase_list[0][1]
                    user_agent = useragent_list[j][2]
                    lib = useragent_list[j][1]
                    worker.submit(send_tracking_data,project=project,distinct_id='batch_send_deduplication'+str(j),url=url,lib=lib,ip=ip,user_agent=user_agent,other_value={'ua字典行数':j,'行计数':indepent_count-1,'应含独立行数':indepent_count,'累计行数':send_count,'本行发送次数':j_count,'本行应该去除数':j_rule_count,'本行不应该去重数':j_count-j_rule_count,'规则':'正常重复数据，重复写入只记1条'},track_id=j,time13=time13,remark=remark,mode=send_mode[0],gzip=send_zip[0],no_bot=no_bot)
                if (j+1)%i == 1:
                    send_recount_count += 1
                    j_count += 1
                    send_count += 1
                    ip = ipbase_list[0][1]
                    user_agent = useragent_list[j][2]
                    lib = useragent_list[j][1]
                    time132 = int(time.time()*1000)+j_count
                    worker.submit(send_tracking_data,project=project,distinct_id='batch_send_deduplication'+str(j),url=url,lib=lib,ip=ip,user_agent=user_agent,other_value={'ua字典行数':j,'行计数':indepent_count-1,'应含独立行数':indepent_count,'累计行数':send_count,'本行重复次数':j_count,'本行应该去除数':j_rule_count,'本行不应该去重数':j_count-j_rule_count,'规则':'track_id一致，上报时间戳不一致，多次重复都应该保留'},track_id=j,time13=time132,remark=remark,no_bot=no_bot)
                if i == 3:
                    send_duplicate_count = send_duplicate_count+j_rule_count
                # write_to_log(filename='test_case',defname='batch_send_deduplication',result='uv:'+str(indepent_count)+',pv:'+str(send_count)+',vv:'+str(j_count))
    time_end = int(time.time()*1000)
    print('batch_send_deduplication执行完毕，用时：',time_end-time_start)
    print('应收到请求数据:',send_count,',如开启去重，应包含正常数据:',indepent_count,',应包含特殊规则数据:',send_recount_count,',如果开启去重，实际去重数量应为:',send_duplicate_count,',如果未开启去重，插入数据应为',send_duplicate_count+indepent_count)
    print(time_start,time_end)
    sql = """SELECT
            remark,JSON_EXTRACT( all_json, '$."规则"' ) AS rule,count(*),count(distinct track_id)
            FROM
            {db} 
            where remark like '%{remark}%'
            GROUP BY
                remark,rule
            order by remark,rule ;""".format(remark=remark,db=project)
    input('根据插入数量等待数据库写入完成后，按回车键查询结果')
    result = do_tidb_select(sql=sql,retrycount=0)
    print(result[0])


def send_tracking_data(mode='post',gzip='yes',project='test_me',distinct_id='test_distinct_id',lib='js',track_id=0,time13=int(time.time()*1000),ip='36.56.48.14',user_agent=admin.who_am_i,url='http://127.0.0.1:5000/',other_value={},remark='normal',no_bot=''):
    data = data_generate(distinct_id=distinct_id,track_id=track_id,lib=lib,time13=time13,other_value=other_value)
    if mode == 'post':
        if gzip == 'yes':
            sent_date = data['dataszip']
        else:
            sent_date = data['datas']
        req = get_anyting_from_postjson(url=url+'sa.gif?project='+project+'&ip='+ip+'&remark='+ remark +'&no_bot='+no_bot \
            ,data={"data_list":sent_date},ua=user_agent)
    if mode == 'get':
        if gzip == 'yes':
            sent_date = data['datazip']
        else:
            sent_date = data['data']
        req = get_anyting_from_get(url=url+'sa.gif?project='+project+'&ip='+ip +'&remark='+ remark +'&data='+sent_date +'&no_bot='+no_bot\
            ,ua=user_agent)
    if req.headers['Content-Type'] == 'image/gif':
        return {'status':'ok','msg':''}
    else:
        return {'status':'fail','msg':req.text}



def test_shortcut(count=1000):
    for i in range(0,count) :
        with ThreadPoolExecutor(max_workers=50) as worker:
            worker.submit(req,id=i)
def req(id):
    result = get_json_from_postjson(url='http://localhost:8000/shortit',data={'org_url':'http://www.{count}.com'.format(count=id)})
    print(result)



if __name__ == '__main__':
    # test_shortcut(count=1000)
    # print(len(test_ip_generate()),len(test_useragent_generate()))
    # batch_send_deduplication(project='test_app',url='http://192.168.193.28:8000/')
    remark2 = sys.argv[1] if sys.argv[1] else 'normal'
    no_bot = sys.argv[2] if sys.argv[2] else ''
    batch_send_deduplication(project='test_me',url='http://192.168.193.28:8000/',remark = remark2, no_bot = no_bot)
    # batch_send_deduplication(project='test_app',url='http://127.0.0.1:8000/',remark = remark2, no_bot = no_bot)

