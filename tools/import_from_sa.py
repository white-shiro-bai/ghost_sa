# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
from configs.sensorsSQL import exesqlsc,exesqlcs
import json
from component.api import insert_data
from component.api_tools import insert_user
from component.db_func import insert_shortcut
from geoip.geo import get_addr,get_asn
from configs.export import write_to_log
import time
import multiprocessing
import pickle
import os
import datetime
import traceback
import urllib

def download_events_from_sa_to_pickle(project='tvcbook',remark='default',start_day='2018-11-27',end_day='2019-09-25'):
    start_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    end_day = datetime.datetime.strptime(end_day, '%Y-%m-%d')
    date_list = []
    date_list.append(start_day.strftime('%Y-%m-%d'))
    while start_day < end_day:
            # 日期叠加一天
            start_day += datetime.timedelta(days=+1)
            # 日期转字符串存入列表
            date_list.append(start_day.strftime('%Y-%m-%d'))
    for day in date_list:
        for hour in range(0,24):
            time_start = day + ' ' + str(hour) + ':00:00.000'
            time_end = day + ' ' + str(hour) + ':59:59.999'
            print(day,str(hour),time_start,time_end) 
            sql="""select * from events where date='{date}' and time >= '{time_start}' and time< '{time_end}'""".format(date=day,time_start=time_start,time_end=time_end)
            results = exesqlcs(sql).splitlines()
            # dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
            dirpath = os.path.join('data_export',project,remark,'events',day)
            os.makedirs(dirpath, exist_ok=True)
            filepath = os.path.join(dirpath , day+'-'+str(hour)+'.pkl')
            with open(filepath,"wb") as f:
                f.write(pickle.dumps(results))

def upload_events_from_pickle_to_sql(project='tvcbook',remark='production'):
    #所有的文件
    filelist = []
    dirpath = os.path.join('data_export',project,remark,'events')
    for maindir, subdir, file_name_list in os.walk(dirpath):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",str(file_name_list))    #当前主目录下的所有文件
        # file_name_list.sort()
        # subdir.sort()
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            filelist.append(apath)
    #     print(file_name_list)
    filelist.sort()
    # print(filelist)
    for pkl in filelist:
        # print(pkl)
        with open(pkl,"rb") as f2:
                    results = pickle._loads(f2.read())
        # p = multiprocessing.Pool(processes = 3)
        for item in results:
            # # print(item)
            try:
                itemdict = json.loads(item)
                all_json = {"properties":itemdict,"distinct_id":itemdict["distinct_id"],"event":itemdict["event"],"type":"track"}
                # first_id = itemdict['first_id'] if 'first_id' in itemdict else None
                # second_id = itemdict['second_id'] if 'second_id' in itemdict else None
                # unionid = itemdict['unionid'] if 'unionid' in itemdict else None
                # id = itemdict['id'] if 'id' in itemdict else None
                ip_city,ip_is_good = get_addr(itemdict["$ip"])
                ip_asn,ip_asn_is_good = get_asn(itemdict["$ip"])
                if ip_is_good ==0:
                    ip_city = '{}'
                if ip_asn_is_good ==0:
                    ip_asn = '{}'
                print(all_json)
                created_at=time.mktime(time.strptime(itemdict["time"].split('.')[0],'%Y-%m-%d %H:%M:%S'))
            # all_json = json.dumps(itemdict,ensure_ascii=False)
                insert_data(project='tvcbook',data_decode=all_json,User_Agent=None,Host=None,Connection=None,Pragma=None,Cache_Control=None,Accept=None,Accept_Encoding=None,Accept_Language=None,ip=itemdict["$ip"] if "$ip" in itemdict else None,ip_city=ip_city,ip_asn=ip_asn,url=None,referrer=itemdict["$referrer"] if "$referrer" in itemdict else None,remark=remark,ua_platform=itemdict["$lib"] if "$lib" in itemdict else None,ua_browser=itemdict["$browser"] if "$browser" in itemdict else None,ua_version=itemdict["$browser_version"] if "$browser_version" in itemdict else None,ua_language=None,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=created_at)
            except Exception:
                error = traceback.format_exc()
                write_to_log(filename='import_from_sa', defname='upload_events_from_pickle_to_sql', result=error)
        # f2.close()
            #     p.apply_async(func=insert_data,kwds={
            #         "project":"tvcbook",
            #         "data_decode":all_json,
            #         "User_Agent":None,
            #         "Host":None,
            #         "Connection":None,
            #         "Pragma":None,
            #         "Cache_Control":None,
            #         "Accept":None,
            #         "Accept_Encoding":None,
            #         "Accept_Language":None,
            #         "ip":itemdict["$ip"] if "$ip" in itemdict else None,
            #         "ip_city":ip_city,
            #         "ip_asn":ip_asn,
            #         "url":None,
            #         "referrer":itemdict["$referrer"] if "$referrer" in itemdict else None,
            #         "remark":'production',
            #         "ua_platform":itemdict["$lib"] if "$lib" in itemdict else None,
            #         "ua_browser":itemdict["$browser"] if "$browser" in itemdict else None,
            #         "ua_version":itemdict["$browser_version"] if "$browser_version" in itemdict else None,
            #         "ua_language":None,
            #         "ip_is_good":ip_is_good,
            #         "ip_asn_is_good":ip_asn_is_good,
            #         "created_at":created_at})
            #     # insert_data
            # p.close()
            # p.join()
        os.remove(pkl)

def upload_events_from_pickle_to_sql_m(project='tvcbook',remark='production',process=8):
    #所有的文件
    filelist = []
    dirpath = os.path.join('data_export',project,remark,'events')
    for maindir, subdir, file_name_list in os.walk(dirpath):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",str(file_name_list))    #当前主目录下的所有文件
        # file_name_list.sort()
        # subdir.sort()
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            filelist.append(apath)
    #     print(file_name_list)
    filelist.sort()
    # print(filelist)
    for pkl in filelist:
        # print(pkl)
        with open(pkl,"rb") as f2:
                    results = pickle._loads(f2.read())
        p = multiprocessing.Pool(processes = process)
        for item in results:
            # # print(item)
            try:
                itemdict = json.loads(item)
                all_json = {"properties":itemdict,"distinct_id":itemdict["distinct_id"],"event":itemdict["event"],"type":"track"}
                # first_id = itemdict['first_id'] if 'first_id' in itemdict else None
                # second_id = itemdict['second_id'] if 'second_id' in itemdict else None
                # unionid = itemdict['unionid'] if 'unionid' in itemdict else None
                # id = itemdict['id'] if 'id' in itemdict else None
                ip_city,ip_is_good = get_addr(itemdict["$ip"])
                ip_asn,ip_asn_is_good = get_asn(itemdict["$ip"])
                if ip_is_good ==0:
                    ip_city = '{}'
                if ip_asn_is_good ==0:
                    ip_asn = '{}'
                # print(all_json)
                created_at=time.mktime(time.strptime(itemdict["time"].split('.')[0],'%Y-%m-%d %H:%M:%S'))
            # all_json = json.dumps(itemdict,ensure_ascii=False)
                # insert_data(project='tvcbook',data_decode=all_json,User_Agent=None,Host=None,Connection=None,Pragma=None,Cache_Control=None,Accept=None,Accept_Encoding=None,Accept_Language=None,ip=itemdict["$ip"] if "$ip" in itemdict else None,ip_city=ip_city,ip_asn=ip_asn,url=None,referrer=itemdict["$referrer"] if "$referrer" in itemdict else None,remark=remark,ua_platform=itemdict["$lib"] if "$lib" in itemdict else None,ua_browser=itemdict["$browser"] if "$browser" in itemdict else None,ua_version=itemdict["$browser_version"] if "$browser_version" in itemdict else None,ua_language=None,ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,created_at=created_at)
                p.apply_async(func=insert_data,kwds={
                    "project":"tvcbook",
                    "data_decode":all_json,
                    "User_Agent":None,
                    "Host":None,
                    "Connection":None,
                    "Pragma":None,
                    "Cache_Control":None,
                    "Accept":None,
                    "Accept_Encoding":None,
                    "Accept_Language":None,
                    "ip":itemdict["$ip"] if "$ip" in itemdict else None,
                    "ip_city":ip_city,
                    "ip_asn":ip_asn,
                    "url":None,
                    "referrer":itemdict["$referrer"] if "$referrer" in itemdict else None,
                    "remark":'production',
                    "ua_platform":itemdict["$lib"] if "$lib" in itemdict else None,
                    "ua_browser":itemdict["$browser"] if "$browser" in itemdict else None,
                    "ua_version":itemdict["$browser_version"] if "$browser_version" in itemdict else None,
                    "ua_language":None,
                    "ip_is_good":ip_is_good,
                    "ip_asn_is_good":ip_asn_is_good,
                    "created_at":created_at})
            except Exception:
                error = traceback.format_exc()
                write_to_log(filename='import_from_sa', defname='upload_events_from_pickle_to_sql', result=error)
        p.close()
        p.join()
        f2.close()
        os.remove(pkl)

def download_users_from_sa_to_pickle(project='tvcbook',remark='production'):
    # start_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    # end_day = datetime.datetime.strptime(end_day, '%Y-%m-%d')
    # date_list = []
    # date_list.append(start_day.strftime('%Y-%m-%d'))
    # while start_day < end_day:
    #         # 日期叠加一天
    #         start_day += datetime.timedelta(days=+1)
    #         # 日期转字符串存入列表
    #         date_list.append(start_day.strftime('%Y-%m-%d'))
    # for day in date_list:
    #     for hour in range(0,24):
    #         time_start = day + ' ' + str(hour) + ':00:00.000'
    #         time_end = day + ' ' + str(hour) + ':59:59.999'
    #         print(day,str(hour),time_start,time_end) 
    sql="""select * from users """#.format(date=day,time_start=time_start,time_end=time_end)
    # results = exesqlcs(sql).splitlines()
    results = exesqlsc(sql).splitlines()
    # dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
    dirpath = os.path.join('data_export',project,remark,'users')
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath , 'users_all.pkl')
    with open(filepath,"wb") as f:
        f.write(pickle.dumps(results))
# def download_users_from_sa_to_pickle(project='tvcbook',remark='production'):
#     # start_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
#     # end_day = datetime.datetime.strptime(end_day, '%Y-%m-%d')
#     # date_list = []
#     # date_list.append(start_day.strftime('%Y-%m-%d'))
#     # while start_day < end_day:
#     #         # 日期叠加一天
#     #         start_day += datetime.timedelta(days=+1)
#     #         # 日期转字符串存入列表
#     #         date_list.append(start_day.strftime('%Y-%m-%d'))
#     # for day in date_list:
#     #     for hour in range(0,24):
#     #         time_start = day + ' ' + str(hour) + ':00:00.000'
#     #         time_end = day + ' ' + str(hour) + ':59:59.999'
#     #         print(day,str(hour),time_start,time_end) 
#     sql="""select * from users """#.format(date=day,time_start=time_start,time_end=time_end)
#     results = exesqlsc(sql).splitlines()
#     # dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
#     dirpath = os.path.join('data_export',project,remark,'users')
#     os.makedirs(dirpath, exist_ok=True)
#     filepath = os.path.join(dirpath , 'users_all.pkl')
#     with open(filepath,"wb") as f:
#         f.write(pickle.dumps(results))

# def import_users(project='tvcbook',remark='production'):
#     sql="""select * from events where date='2019-11-18' and time< '2019-11-18 01:00:00.000'"""
#     results = exesqlsc(sql).splitlines()
#     # p = multiprocessing.Pool(processes = 3)
#     for item in results:


# def upload_users_from_pickle_to_sql(project='tvcbook',remark='default'):
def upload_users_from_pickle_to_sql(project='tvcbook',remark='production'):
    dirpath = os.path.join('data_export',project,remark,'users')
    filepath = os.path.join(dirpath , 'users_all.pkl')
    with open(filepath,"rb") as f2:
        results = pickle._loads(f2.read())
    a = 1
    for item in results:
        print(a)
        a += 1
        # print('a',item)
        data_rebuild = {"properties":{},"lib":{},"distinct_id":"","event":"","type":"profile_set"}
        # print(item)
        try:
            item = json.loads(item)
        # print(item["first_id"])
            if len(item["first_id"])==16:
                data_rebuild['lib']['$lib'] = 'js'
            elif len(item['first_id'])>=39 and len(item['first_id'])<=46:
                data_rebuild['lib']['$lib'] = 'MiniProgram'
            elif len(item['first_id'])>=51 and len(item['first_id'])<=64:
                data_rebuild['lib']['$lib'] = 'js'
            else:
                data_rebuild['lib']['$lib'] = 'unknow'


            if 'second_id' in item:
                data_rebuild["distinct_id"] = item['second_id']
                data_rebuild["map_id"] = item['first_id']
                data_rebuild["original_id"] = item['first_id']
                if 'userid' in item:
                    # data_rebuild["properties"]["user_id"] = item['userid']
                    data_rebuild["properties"]["userId"] = item['userid']
                if 'name' in item:
                    data_rebuild["properties"]["name"] = item['name']
                if 'realname' in item:
                    data_rebuild["properties"]["realname"] = item['realname']
                if 'sex' in item:
                    data_rebuild["properties"]["sex"] = item['sex']
                if 'verification_type' in item:
                    data_rebuild["properties"]["verification_type"] = item['verification_type']
                if 'company' in item:
                    data_rebuild["properties"]["company"] = item['company']
            # print(item)
            else:
                data_rebuild["distinct_id"] = item['first_id']
                # data_rebuild["map_id"] = item['first_id']
                # data_rebuild["original_id"] = item['first_id']
                if 'userid' in item:
                    # data_rebuild["properties"]["user_id"] = item['userid']
                    data_rebuild["properties"]["userId"] = item['userid']
                if 'name' in item:
                    data_rebuild["properties"]["name"] = item['name']
                if 'realname' in item:
                    data_rebuild["properties"]["realname"] = item['realname']
                if 'sex' in item:
                    data_rebuild["properties"]["sex"] = item['sex']
                if 'verification_type' in item:
                    data_rebuild["properties"]["verification_type"] = item['verification_type']
                if 'company' in item:
                    data_rebuild["properties"]["company"] = item['company']
                if 'viptype' in item:
                    data_rebuild["properties"]["viptype"] = item['viptype']
            print(data_rebuild)
            insert_user(project='tvcbook',data_decode=data_rebuild,created_at=0)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='import_from_sa', defname='upload_users_from_pickle_to_sql', result=error)
    os.remove(filepath)


def import_shortcut_from_sa_to_sql(project='your_project_name',domain='your_domain'):
    sql = """select $short_url_key,$short_url_target from events where event='$ShortUrlRedirect' group by $short_url_key,$short_url_target"""
    # result = exesqlcs(sql).splitlines()
    result = exesqlsc(sql).splitlines()
    count = 1
    for i in result:
        print (count)
        count +=1
        fi = json.loads(i)
        short_url_target = urllib.parse.unquote(fi["$short_url_target"])
        short_url_key = fi["$short_url_key"]
        utm_source =None
        utm_medium =None
        utm_campaign=None
        utm_content=None
        utm_term=None
        for params in short_url_target.split('?')[-1].split('&'):
            if 'utm_source' in params:
                utm_source = params.replace('utm_source=','')
            if 'utm_medium' in params:
                utm_medium = params.replace('utm_medium=','')
            if 'utm_campaign' in params:
                utm_campaign = params.replace('utm_campaign=','')
            if 'utm_content' in params:
                utm_content = params.replace('utm_content=','')
            if 'utm_term' in params:
                utm_term = params.replace('utm_term=','')
        insert_shortcut(project=project,short_url=short_url_key,long_url=short_url_target,expired_at=2147443200,src='sensors',src_short_url=domain+short_url_key,submitter='importer',utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term)


if __name__ == "__main__":
        # import_events()
    # import_events_to_pickle()
    # download_events_from_sa_to_pickle()
    # upload_events_from_pickle_to_sql()
    upload_events_from_pickle_to_sql_m()
    # download_events_from_sa_to_pickle_speciallist()
    # download_users_from_sa_to_pickle()
    # upload_users_from_pickle_to_sql()
    # upload_users_from_pickle_to_sql(project='tvcbook',remark='default')
    # upload_users_from_pickle_to_sql(project='tvcbook',remark='production')
    # import_shortcut_from_sa_to_sql()