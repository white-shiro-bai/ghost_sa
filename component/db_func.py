# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.path.append("./")
sys.setrecursionlimit(10000000)
import time
from component.db_op import do_tidb_exe,do_tidb_select
from configs.export import write_to_log
from configs import admin
import traceback

def insert_event(table,alljson,track_id,distinct_id,lib,event,type_1,User_Agent,Host,Connection,Pragma,Cache_Control,Accept,Accept_Encoding,Accept_Language,ip,ip_city,ip_asn,url,referrer,ua_platform,ua_browser,ua_version,ua_language,remark='normal',created_at=None):
    if created_at is None:
        timenow = int(time.time())
        date = time.strftime("%Y-%m-%d", time.localtime())
        hour = int(time.strftime("%H", time.localtime()))
    else:
        timenow = created_at
        date = time.strftime("%Y-%m-%d", time.localtime(created_at))
        hour = int(time.strftime("%H", time.localtime(created_at)))
    sql = """insert HIGH_PRIORITY into `{table}` (`all_json`,`track_id`,`distinct_id`,`lib`,`event`,`type`,`created_at`,`date`,`hour`,`user_agent`,`host`,`connection`,`pragma`,`cache_control`,`accept`,`accept_encoding`,`accept_language`,`ip`,`ip_city`,`ip_asn`,`url`,`referrer`,`remark`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`) values (%(alljson)s,%(track_id)s,%(distinct_id)s,%(lib)s,%(event)s,%(type)s,%(created_at)s,%(date)s,%(hour)s,%(User_Agent)s,%(Host)s,%(Connection)s,%(Pragma)s,%(Cache_Control)s,%(Accept)s,%(Accept_Encoding)s,%(Accept_Language)s,%(ip)s,%(ip_city)s,%(ip_asn)s,%(url)s,%(referrer)s,%(remark)s,%(ua_platform)s,%(ua_browser)s,%(ua_version)s,%(ua_language)s)""".format(table=table)
    key = {'alljson':alljson,'track_id':track_id,'distinct_id':distinct_id,'lib':lib,'event':event,'type':type_1,'created_at':timenow,'date':date,'hour':hour,'User_Agent':User_Agent,'Host':Host,'Connection':Connection,'Pragma':Pragma,'Cache_Control':Cache_Control,'Accept':Accept,'Accept_Encoding':Accept_Encoding,'Accept_Language':Accept_Language,'ip':ip,'ip_city':ip_city,'ip_asn':ip_asn,'url':url,'referrer':referrer,'remark':remark,'ua_platform':ua_platform,'ua_browser':ua_browser,'ua_version':ua_version,'ua_language':ua_language}
    result = do_tidb_exe(sql=sql, args=key)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='insert_event',result=result+sql+str(key))
    return result[1]


def insert_devicedb(table,distinct_id,device_id,manufacturer,model,os,os_version,screen_width,screen_height,network_type,user_agent,accept_language,ip,ip_city,ip_asn,wifi,app_version,carrier,referrer,referrer_host,bot_name,browser,browser_version,is_login_id,screen_orientation,gps_latitude,gps_longitude,first_visit_time,first_referrer,first_referrer_host,first_browser_language,first_browser_charset,first_search_keyword,first_traffic_source_type,utm_content,utm_campaign,utm_medium,utm_term,utm_source,latest_utm_content,latest_utm_campaign,latest_utm_medium,latest_utm_term,latest_utm_source,latest_referrer,latest_referrer_host,latest_search_keyword,latest_traffic_source_type,update_content,ua_platform,ua_browser,ua_version,ua_language,lib,created_at=None,updated_at=None):
    if created_at is None:
        timenow = int(time.time())
        date = time.strftime("%Y-%m-%d", time.localtime())
        hour = int(time.strftime("%H", time.localtime()))
    else:
        timenow = created_at
        date = time.strftime("%Y-%m-%d", time.localtime(created_at))
        hour = int(time.strftime("%H", time.localtime(created_at)))
    sql = """set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 10;
    insert HIGH_PRIORITY into `{table}_device` (`distinct_id`,`device_id`,`manufacturer`,`model`,`os`,`os_version`,`screen_width`,`screen_height`,`network_type`,`user_agent`,`accept_language`,`ip`,`ip_city`,`ip_asn`,`wifi`,`app_version`,`carrier`,`referrer`,`referrer_host`,`bot_name`,`browser`,`browser_version`,`is_login_id`,`screen_orientation`,`gps_latitude`,`gps_longitude`,`first_visit_time`,`first_referrer`,`first_referrer_host`,`first_browser_language`,`first_browser_charset`,`first_search_keyword`,`first_traffic_source_type`,`utm_content`,`utm_campaign`,`utm_medium`,`utm_term`,`utm_source`,`latest_utm_content`,`latest_utm_campaign`,`latest_utm_medium`,`latest_utm_term`,`latest_utm_source`,`latest_referrer`,`latest_referrer_host`,`latest_search_keyword`,`latest_traffic_source_type`,`created_at`,`updated_at`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`,`lib`) values ( %(distinct_id)s,%(device_id)s,%(manufacturer)s,%(model)s,%(os)s,%(os_version)s,%(screen_width)s,%(screen_height)s,%(network_type)s,%(user_agent)s,%(accept_language)s,%(ip)s,%(ip_city)s,%(ip_asn)s,%(wifi)s,%(app_version)s,%(carrier)s,%(referrer)s,%(referrer_host)s,%(bot_name)s,%(browser)s,%(browser_version)s,%(is_login_id)s,%(screen_orientation)s,%(gps_latitude)s,%(gps_longitude)s,%(first_visit_time)s,%(first_referrer)s,%(first_referrer_host)s,%(first_browser_language)s,%(first_browser_charset)s,%(first_search_keyword)s,%(first_traffic_source_type)s,%(utm_content)s,%(utm_campaign)s,%(utm_medium)s,%(utm_term)s,%(utm_source)s,%(latest_utm_content)s,%(latest_utm_campaign)s,%(latest_utm_medium)s,%(latest_utm_term)s,%(latest_utm_source)s,%(latest_referrer)s,%(latest_referrer_host)s,%(latest_search_keyword)s,%(latest_traffic_source_type)s,%(created_at)s,%(updated_at)s,%(ua_platform)s,%(ua_browser)s,%(ua_version)s,%(ua_language)s,%(lib)s) ON DUPLICATE KEY UPDATE `updated_at`={updated_at}{update_content};""".format(table=table,updated_at=timenow,update_content=update_content)
    key = {'distinct_id':distinct_id,'device_id':device_id,'manufacturer':manufacturer,'model':model,'os':os,'os_version':os_version,'screen_width':screen_width,'screen_height':screen_height,'network_type':network_type,'user_agent':user_agent,'accept_language':accept_language,'ip':ip,'ip_city':ip_city,'ip_asn':ip_asn,'wifi':wifi,'app_version':app_version,'carrier':carrier,'referrer':referrer,'referrer_host':referrer_host,'bot_name':bot_name,'browser':browser,'browser_version':browser_version,'is_login_id':is_login_id,'screen_orientation':screen_orientation,'gps_latitude':gps_latitude,'gps_longitude':gps_longitude,'first_visit_time':first_visit_time,'first_referrer':first_referrer,'first_referrer_host':first_referrer_host,'first_browser_language':first_browser_language,'first_browser_charset':first_browser_charset,'first_search_keyword':first_search_keyword,'first_traffic_source_type':first_traffic_source_type,'utm_content':utm_content,'utm_campaign':utm_campaign,'utm_medium':utm_medium,'utm_term':utm_term,'utm_source':utm_source,'latest_utm_content':latest_utm_content,'latest_utm_campaign':latest_utm_campaign,'latest_utm_medium':latest_utm_medium,'latest_utm_term':latest_utm_term,'latest_utm_source':latest_utm_source,'latest_referrer':latest_referrer,'latest_referrer_host':latest_referrer_host,'latest_search_keyword':latest_search_keyword,'latest_traffic_source_type':latest_traffic_source_type,'created_at':timenow,'updated_at':timenow,'ua_platform':ua_platform,'ua_browser':ua_browser,'ua_version':ua_version,'ua_language':ua_language,'lib':lib}
    result = do_tidb_exe(sql=sql, args=key)
    return result[1]

def insert_user_db(project,distinct_id,lib,map_id,original_id,user_id,all_user_profile,update_params,created_at=None,updated_at=None):
    if created_at is None:
        timenow = int(time.time())
        date = time.strftime("%Y-%m-%d", time.localtime())
        hour = int(time.strftime("%H", time.localtime()))
    else:
        timenow = created_at
        date = time.strftime("%Y-%m-%d", time.localtime(created_at))
        hour = int(time.strftime("%H", time.localtime(created_at)))
    sql = """set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 10;
    insert HIGH_PRIORITY into `{table}_user` (`distinct_id`,`lib`,`map_id`,`original_id`,`user_id`,`all_user_profile`,`created_at`,`updated_at`) values (%(distinct_id)s,%(lib)s,%(map_id)s,%(original_id)s,%(user_id)s,%(all_user_profile)s,%(created_at)s,%(updated_at)s) ON DUPLICATE KEY UPDATE `updated_at`={updated_at}{update_params}""".format(table=project,update_params=update_params,updated_at=timenow)
    key={'distinct_id':distinct_id,'lib':lib,'map_id':map_id,'original_id':original_id,'user_id':user_id,'all_user_profile':all_user_profile,'created_at':timenow,'updated_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result[1]


def insert_properties(project,lib,remark,event,properties,properties_len,created_at=None,updated_at=None):
    if created_at is None:
        created_at = int(time.time())
    if updated_at is None:
        updated_at = int(time.time())
    sql = """set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 10;
    insert HIGH_PRIORITY into `{table}_properties` (`lib`,`remark`,`event`,`properties`,`properties_len`,`created_at`,`updated_at`,`total_count`,`lastinsert_at`) values ( %(lib)s,%(remark)s,%(event)s,%(properties)s,%(properties_len)s,%(created_at)s,%(updated_at)s,1,%(updated_at)s) ON DUPLICATE KEY UPDATE `properties`=if(properties_len<%(properties_len)s,%(properties)s,properties),`properties_len`=if(properties_len<%(properties_len)s,%(properties_len)s,properties_len),updated_at=if(properties_len<%(properties_len)s,%(updated_at)s,updated_at),total_count=total_count+1,lastinsert_at=%(updated_at)s;""".format(table=project)
    key = {'lib':lib,'remark':remark,'event':event,'properties':properties,'properties_len':properties_len,'created_at':created_at,'updated_at':updated_at}
    result = do_tidb_exe(sql=sql, args=key)

def check_user_device(project,distinct_id,first_id):
    #仅用于导入神策旧数据
    sql = """select first_id,second_id from users where first_id = '{first_id}'""".format(first_id=first_id)



def get_long_url_from_short(short_url):
    timenow = int(time.time())
    sql = """select HIGH_PRIORITY long_url,expired_at from shortcut where short_url ='{shorturl}' order by expired_at desc""".format(shorturl=short_url)
    result = do_tidb_select(sql)
    if result[1]>0:
        long_url = result[0][0][0]
        expired_at    = result[0][0][1]
        if expired_at is None or expired_at > timenow :
            return long_url,'success'
        else:
            return '','expired'
    else:
        return '','fail'

def check_long_url(long_url):
    timenow = int(time.time())
    sql = """select project,short_url,from_unixtime(expired_at),from_unixtime(created_at),src,src_short_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term,long_url from shortcut where long_url = '{long_url}' and expired_at > {timenow}""".format(long_url=long_url,timenow=timenow)
    result = do_tidb_select(sql)
    if result[1] >0:
        result_dict = []
        for item in result[0]:
            project = item[0]
            short_url = item[1]
            expired_at = item[2]
            created_at = item[3]
            src = item[4]
            src_short_url = item[5]
            submitter = item[6]
            utm_source = item[7]
            utm_medium = item[8]
            utm_campaign = item[9]
            utm_content = item[10]
            utm_term = item[11]
            long_url = item[12]
            result_dict.append({'project':project,'short_url':short_url,'expired_at':expired_at,'created_at':created_at,'src':src,'src_short_url':src_short_url,'submitter':submitter,'utm_source':utm_source,'utm_medium':utm_medium,'utm_campaign':utm_campaign,'utm_content':utm_content,'utm_term':utm_term,'long_url':long_url})
        return result_dict,'exist'
    else:
        return '','empty'

def insert_shortcut(project,short_url,long_url,expired_at,src,src_short_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term):
    timenow = int(time.time())
    sql = """insert into shortcut (`project`,`short_url`,`long_url`,`expired_at`,`created_at`,`src`,`src_short_url`,`submitter`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{project}','{short_url}','{long_url}',{expired_at},{created_at},'{src}','{src_short_url}','{submitter}','{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}')""".format(project=project,short_url=short_url,long_url=long_url,expired_at=expired_at,created_at=timenow,src=src,src_short_url=src_short_url,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
    result = do_tidb_exe(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='insert_shortcut',result=result+sql)
    return result[1]



def show_shortcut(page,length,filters='',sort='`shortcut`.created_at',way='desc'):
    sql = """SELECT `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at,count(shortcut_history.created_at) as visit_times,count(shortcut_read.created_at) as read_times FROM `shortcut` left join `shortcut_history` on `shortcut`.short_url = `shortcut_history`.`short_url`    left join `shortcut_read` on `shortcut`.short_url = `shortcut_read`.`short_url` {filters} GROUP BY `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at ORDER BY {sort} {way} Limit {start_pageline},{length}""".format(start_pageline=(page-1)*length if page>1 else 0,length=length,filters=filters,sort=sort,way=way)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='show_shortcut',result=str(result)+sql)
        return '',0
    return result[0],result[1]

def count_shortcut(filters=''):
    sql = """SELECT count(*) FROM `shortcut` {filters} """.format(filters=filters)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='show_shortcut',result=str(result)+sql)
        return '',0
    return result[0]


def insert_shortcut_history(short_url,result,cost_time,ip,user_agent,accept_language,ua_platform,ua_browser,ua_version,ua_language,created_at=None):
    timenow = int(time.time())
    sql = """insert HIGH_PRIORITY shortcut_history (`short_url`,`result`,`cost_time`,`ip`,`created_at`,`user_agent`,`accept_language`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`) values ('{short_url}','{result}',{cost_time},'{ip}',{created_at},'{user_agent}','{accept_language}','{ua_platform}','{ua_browser}','{ua_version}','{ua_language}')""".format(short_url=short_url,result=result,cost_time=cost_time,ip=ip,created_at= created_at if created_at else timenow,user_agent=user_agent,accept_language=accept_language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language).replace("'None'","Null").replace("None","Null")
    result = do_tidb_exe(sql)
    print('已插入解析记录'+str(result[1]))

def show_check(project,date,hour,order,start,limit,add_on_where):
    sql = """select distinct_id,event,type,all_json,host,user_agent,ip,url,remark,from_unixtime(created_at) from {project} where date = '{date}' and hour = {hour} {add_on_where} order by created_at {order} limit {start},{limit}""".format(project=project,date=date,hour=hour,order=order,start=start,limit=limit,add_on_where=add_on_where)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='show_check',result=str(result)+sql)
        return '',0
    return result[0],result[1]

def show_project():
    sql = """select project_name,FROM_UNIXTIME(created_at),FROM_UNIXTIME(expired_at),enable_scheduler from project_list order by project_name"""
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='show_project',result=str(result)+sql)
        return '',0
    return result[0],result[1]

def insert_mobile_ad_src(src,src_name,src_args,utm_source,utm_medium,utm_campaign,utm_content,utm_term):
    timenow = int(time.time())
    sql = """insert mobile_ad_src (`src`,`src_name`,`src_args`,`created_at`,`updated_at`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{src}','{src_name}','{src_args}',{created_at},{updated_at},'{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}') ON DUPLICATE KEY UPDATE `src_name`='{src_name}',`src_args`='{src_args}',`updated_at`={updated_at},`utm_source`='{utm_source}',`utm_medium`='{utm_medium}',`utm_campaign`='{utm_campaign}',`utm_content`='{utm_content}',`utm_term`='{utm_term}' """.format(src=src,src_name=src_name,src_args=src_args,created_at=timenow,updated_at=timenow,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
    result = do_tidb_exe(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='insert_mobile_ad_src',result=str(result)+sql)
        return '',0
    return result[0],result[1]



def insert_mobile_ad_list(project,url,src,src_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term,expired_at=2147483647):
    timenow = int(time.time())
    sql="""insert mobile_ad_list (`project`,`url`,`expired_at`,`created_at`,`src`,`src_url`,`submitter`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{project}','{url}',{expired_at},{created_at},'{src}','{src_url}','{submitter}','{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}')""".format(project=project,url=url,expired_at=expired_at,created_at=timenow,src=src,src_url=src_url,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
    result = do_tidb_exe(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='insert_mobile_ad_list',result=str(result)+sql)
        return '',0
    return result[0],result[1]

def read_mobile_ad_list(page,length,filters='',sort='created_at',way='desc'):
    sort = 'mobile_ad_list.'+ sort
    sql ="""select mobile_ad_list.project,
    mobile_ad_list.url,
    mobile_ad_list.src,
    mobile_ad_src.src_name,
    mobile_ad_list.src_url,
    mobile_ad_list.submitter,
    mobile_ad_list.utm_source,
    mobile_ad_list.utm_medium,
    mobile_ad_list.utm_campaign,
    mobile_ad_list.utm_content,
    mobile_ad_list.utm_term,
    from_unixtime(mobile_ad_list.created_at,'%Y-%m-%d'),
    from_unixtime(mobile_ad_list.expired_at,'%Y-%m-%d')
    from mobile_ad_list left join mobile_ad_src on mobile_ad_list.src=mobile_ad_src.src {filters} ORDER BY {sort} {way} Limit {start_pageline},{length}""".format(start_pageline=(page-1)*length,length=length,filters=filters,sort=sort,way=way)
    print(sql)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='read_mobile_ad_list',result=str(result)+sql)
        return '',0
    return result[0],result[1]


def count_mobile_ad_list(filters=''):
    sql = """SELECT count(*) FROM `mobile_ad_list` {filters} """.format(filters=filters)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='count_mobile_ad_list',result=str(result)+sql)
        return '',0
    return result[0]

def read_mobile_ad_src_list(add_on_where=''):
    timenow = int(time.time())
    sql = """select src,src_name,src_args,from_unixtime(created_at),from_unixtime(updated_at),if({timenow}-created_at<=604800,1,0),utm_source,utm_medium,utm_campaign,utm_content,utm_term from mobile_ad_src {add_on_where} order by src_name""".format(add_on_where=add_on_where,timenow=timenow)
    result = do_tidb_select(sql)
    if result[1] == 0:
        write_to_log(filename='db_func',defname='read_mobile_ad_src_list',result=str(result)+sql)
        return '',0
    return result[0],result[1]

def check_mobile_ad_url(url):
    timenow = int(time.time())
    sql = """select project,url,from_unixtime(expired_at),from_unixtime(created_at),src,src_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term from mobile_ad_list where url = '{url}' and expired_at > {timenow}""".format(url=url,timenow=timenow)
    result = do_tidb_select(sql)
    if result[1]>0:
        result_dict = []
        for item in result[0]:
            result_dict.append({'project':item[0],'url':item[1],'expired_at':item[2],'created_at':item[3],'src':item[4],'src_url':item[5],'submitter':item[6],'utm_source':item[7],'utm_medium':item[8],'utm_campaign':item[9],'utm_content':item[10],'utm_term':item[11]})
        return result_dict,'exist'
    else:
        return '','empty'

def distinct_id_query(distinct_id,project):
    sql = """SELECT 1 FROM {project} where distinct_id ='{distinct_id}' limit 1""".format(distinct_id=distinct_id,project=project)
    result = do_tidb_select(sql)
    return result[1]

def find_recall_url(project,device_id,created_at):
    date = time.strftime("%Y-%m-%d", time.localtime(created_at))
    sql = """select JSON_EXTRACT(all_json,'$."properties"."callback_url"'),all_json,distinct_id from {project} where date >= DATE_SUB('{date}',INTERVAL {day_diff} day) and date <= '{date}' and `event` = '$AppChannelMatching' and distinct_id in ('{device_id}',md5('{device_id}'),replace('{device_id}','"',''),md5(replace('{device_id}','"',''))) order by created_at desc limit 1""".format(project=project,device_id=device_id,date=date,day_diff=admin.aso_dsp_callback_interval_days)
    result = do_tidb_select(sql)
    return result[0],result[1]

def find_recall_history(project,device_id,created_at):
    date = time.strftime("%Y-%m-%d", time.localtime(created_at))
    sql = """select count(1) from {project} where date >= DATE_SUB('{date}',INTERVAL {day_diff}    day) and date <= '{date}' and `event` = '$is_channel_callback_event' and distinct_id in ('{device_id}',md5('{device_id}'),replace('{device_id}','"',''),md5(replace('{device_id}','"','')))""".format(project=project,device_id=device_id,date=date,day_diff=admin.aso_dsp_callback_interval_days)
    result = do_tidb_select(sql)
    return result[0][0][0]

def check_utm(project,distinct_id):
    sql = """select distinct_id,
lib,
utm_content,
utm_campaign,
utm_medium,
utm_term,
utm_source,
latest_utm_content,
latest_utm_campaign,
latest_utm_medium,
latest_utm_term,
latest_utm_source,
first_traffic_source_type,
latest_traffic_source_type
from {project}_device where distinct_id = '{distinct_id}'""".format(project=project,distinct_id=distinct_id)
    result = do_tidb_select(sql)
    return result[0],result[1]

def insert_shortcut_read(short_url,ip,user_agent,accept_language,ua_platform,ua_browser,ua_version,ua_language,referrer,created_at=None):
    timenow = int(time.time())
    sql = """insert HIGH_PRIORITY shortcut_read (`short_url`,`ip`,`created_at`,`user_agent`,`accept_language`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`,`referrer`) values ('{short_url}','{ip}',{created_at},'{user_agent}','{accept_language}','{ua_platform}','{ua_browser}','{ua_version}','{ua_language}','{referrer}')""".format(short_url=short_url,ip=ip,created_at=created_at if created_at else timenow,user_agent=user_agent,accept_language=accept_language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,referrer=referrer).replace("'None'","Null").replace("None","Null")
    result = do_tidb_exe(sql)
    print('已插入解析记录'+str(result[1]))
    
def insert_usergroup_data(project,group_list_id,data_index,key,json,enable,created_at=None,updated_at=None):
    timenow = int(time.time())
    sql = """insert {project}_usergroup_data (`group_list_id`,`data_index`,`data_key`,`data_json`,`enable`,`created_at`,`updated_at`) values (%(group_list_id)s,%(data_index)s,%(data_key)s,%(data_json)s,%(enable11)s,%(created_at)s,%(updated_at)s)""".format(project=project)
    key = {'group_list_id':group_list_id,'data_index':data_index,'data_key':key,'data_json':json,'enable11':enable,'created_at':created_at if created_at else timenow,'updated_at':updated_at if updated_at else timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result[1]

def insert_usergroup_list(project,group_id,group_index,list_desc=None,list_init_date=None,status=0,complete_at=0,apply_temple_times=0,item_add=0,created_at=None,updated_at=None,jobs_id=0):
    timenow = int(time.time())
    sql = """insert {project}_usergroup_list (`group_id`,`group_list_index`,`list_init_date`,`list_desc`,`item_count`,`status`,`complete_at`,`apply_temple_times`,`created_at`,`updated_at`,`jobs_id`) values ({group_id},{group_index},{list_init_date},'{list_desc}',{item_add},{status},{complete_at},{apply_temple_times},{created_at},{updated_at},{jobs_id}) ON DUPLICATE KEY UPDATE `complete_at`=if({complete_at}=0,`complete_at`,{complete_at}),`apply_temple_times`=`apply_temple_times`+{apply_temple_times},`status`=if ({status}=0,`status`,{status}),`item_count`=if({item_add}=0,`item_count`,`item_count`+{item_add}),updated_at={updated_at}""".format(project=project,jobs_id=jobs_id,group_id=group_id,group_index=group_index,list_init_date=list_init_date if list_init_date else timenow,list_desc=list_desc,status=status,complete_at=complete_at,apply_temple_times=apply_temple_times,item_add=item_add,created_at=created_at if created_at else timenow,updated_at=updated_at if updated_at else timenow)
    result = do_tidb_exe(sql=sql)
    return result[0]

def update_usergroup_plan(project,plan_id,latest_data_list_index=0,latest_apply_temple_time=0,latest_apply_temple_id=0,updated_at=None,repeat_times_add=0,latest_data_time=0):
    timenow = int(time.time())
    sql = """update {project}_usergroup_plan set 
    `latest_data_list_index`=if({latest_data_list_index}=0,`latest_data_list_index`,{latest_data_list_index}),
    `latest_data_time`=if(`latest_data_time`=0,`latest_data_time`,{latest_data_time}),
    `repeat_times`=if(`repeat_times` is null,0+{repeat_times_add},`repeat_times`+{repeat_times_add}),
    `latest_apply_temple_id`=if({latest_apply_temple_id}=0,`latest_apply_temple_id`,{latest_apply_temple_id}),
    `latest_apply_temple_time`={latest_apply_temple_time},updated_at={updated_at}
    where id ={plan_id}""".format(project=project,plan_id=plan_id,latest_data_list_index=latest_data_list_index,latest_apply_temple_time=latest_apply_temple_time,latest_apply_temple_id=latest_apply_temple_id,updated_at=updated_at if updated_at else timenow,repeat_times_add=repeat_times_add,latest_data_time=latest_data_time)
    result = do_tidb_exe(sql=sql)
    return result[0],result[1]


def update_usergroup_list(project,list_id,apply_temple_times,updated_at=None):
    sql = """update {project}_usergroup_list set apply_temple_times=apply_temple_times+{apply_temple_times},updated_at={updated_at} where id={list_id}""".format(apply_temple_times=int(apply_temple_times) if int(apply_temple_times) else 0,project=project,updated_at=updated_at if updated_at else int(time.time()),list_id=list_id)
    result = do_tidb_exe(sql=sql)
    return result[0],result[1]

def check_lastest_usergroup_list_index(project,group_id):
    sql = """select max(group_list_index) from {project}_usergroup_list where group_id={group_id}""".format(project=project,group_id=group_id)
    result = do_tidb_exe(sql=sql)
    if result[1]<1:
        max_count = 0
    elif result[0][0][0] is None:
        max_count = 0
    else:
        max_count = result[0][0][0]
    return max_count

def check_list_id(project,group_id,group_list_index):
    sql = """select id,item_count,status from {project}_usergroup_list where group_id={group_id} and group_list_index={group_list_index}""".format(project=project,group_id=group_id,group_list_index=group_list_index)
    result = do_tidb_exe(sql=sql)
    return result[0]

def check_next_scheduler_job(priority=13,current_time=None):
    current_time=int(time.time()) if not current_time else current_time
    if priority == 13 :
        priorities = '13,14,15'
    elif priority == 14 :
        priorities = '14,15'
    sql = """select id,project,group_id,datetime,data from scheduler_jobs where priority={priority} and datetime<={current_time}  and `status` = 16 order by id limit 1""".format(priority=priority,current_time=current_time)
    result = do_tidb_exe(sql=sql)
    return result[0],result[1]

def update_scheduler_job(jobid,list_index=0,status=0):
    sql="""update scheduler_jobs set list_index = if({list_index}!=0,{list_index},list_index),status=if({status}!=0,{status},status),updated_at={updated_at} where id = {jobid}""".format(jobid=jobid,list_index=list_index,status=status,updated_at=int(time.time()))
    result = do_tidb_exe(sql=sql)
    return result[0],result[1]

def insert_scheduler_job(project,group_id,datetime,data={},priority=13,status=11):
    import json
    sql = """insert ignore scheduler_jobs (`project`,`group_id`,`datetime`,`data`,`priority`,`status`,`created_at`,`updated_at`) values ('{project}',{group_id},{datetime},'{data}',{priority},{status},{created_at},{updated_at})""".format(project=project,group_id=group_id,datetime=datetime,data=json.dumps(data),priority=priority,status=status,created_at=int(time.time()),updated_at=int(time.time()))
    result = do_tidb_exe(sql=sql)
    return result[0],result[1]

def select_scheduler_enable_project():
    sql = """select project_name from project_list where enable_scheduler = 1"""
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_all_project():
    sql = """select project_name from project_list"""
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_usergroup_jobs_plan(project):
    sql = """select id,func,repeatable,priority,enable_policy from {project}_usergroup_plan where enable_policy in (8,28)""".format(project=project)
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_usergroup_jobs_plan_manual(project,plan_id):
    sql = """select id,func,repeatable,priority from {project}_usergroup_plan where id={plan_id}""".format(project=project,plan_id=int(plan_id))
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_usergroup_data(project,group_list_id):
    #整组选择要套模板的分群
    sql = f"""SELECT
    {project}_usergroup_list.group_id,
    {project}_usergroup_list.id,
    {project}_usergroup_data.id,
    {project}_usergroup_data.data_index,
    {project}_usergroup_data.data_key,
    {project}_usergroup_data.data_json,
    {project}_usergroup_data.`enable`
FROM
    {project}_usergroup_data left join {project}_usergroup_list on {project}_usergroup_data.group_list_id={project}_usergroup_list.id
WHERE
    group_list_id = {group_list_id} and {project}_usergroup_data.enable != 10 """
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_usergroupdata_data(project,data_id):
    #选择单个要套模板的人
    sql = f"""SELECT
    {project}_usergroup_list.group_id,
    {project}_usergroup_list.id,
    {project}_usergroup_data.id,
    {project}_usergroup_data.data_index,
    {project}_usergroup_data.data_key,
    {project}_usergroup_data.data_json,
    {project}_usergroup_data.`enable`
FROM
    {project}_usergroup_data left join {project}_usergroup_list on {project}_usergroup_data.group_list_id={project}_usergroup_list.id
WHERE
    {project}_usergroup_data.id = {data_id} and {project}_usergroup_data.enable != 10"""
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def insert_noti(project,type_1,created_at,updated_at,distinct_id,content,send_at,plan_id=0,list_id=0,data_id=0,temple_id=0,noti_group_id=0,priority=13,status=9,owner='noti',recall_result=None,key=None,level=None):
    import json
    sql = """insert ignore {project}_noti (`distinct_id`,`plan_id`,`list_id`,`data_id`,`temple_id`,`noti_group_id`,`priority`,`status`,`owner`,`type`,`content`,`send_at`,`recall_result`,`created_at`,`updated_at`,`key`,`level`) values (%(distinct_id)s,%(plan_id)s,%(list_id)s,%(data_id)s,%(temple_id)s,%(noti_group_id)s,%(priority)s,%(status)s,%(owner)s,%(type)s,%(content)s,%(send_at)s,%(recall_result)s,%(created_at)s,%(updated_at)s,%(key)s,%(level)s)""".format(project=project)
    key = {'key':key,'distinct_id':distinct_id,'type':type_1,'plan_id':plan_id,'list_id':list_id,'data_id':data_id,'temple_id':temple_id,'noti_group_id':noti_group_id,'priority':priority,'status':status,'owner':owner,'content':json.dumps(content),'recall_result':recall_result,'send_at':send_at if send_at else int(time.time()),'created_at':created_at if created_at else int(time.time()),'updated_at':updated_at if updated_at else int(time.time()),'level':level}
    result = do_tidb_exe(sql=sql, args=key)
    return result[0],result[1]

def update_noti(project,noti_id,updated_at,status=0,recall_result=None):
    sql = """update {project}_noti set status = if({status}=0,status,{status}) , recall_result = %(recall_result)s , updated_at = {updated_at} where id = {noti_id}""".format(project=project,noti_id=noti_id,updated_at = updated_at if updated_at else int(time.time()),status=status,recall_result=recall_result)
    key = {"recall_result":recall_result}
    result = do_tidb_exe(sql=sql,args=key)
    return result[0],result[1]

def select_noti_auto(project,priority=13,status=8):
    sql = """select id,noti_group_id,type,content,distinct_id from {project}_noti where status={status} and priority={priority} and send_at<={send_at} limit 1""".format(project=project,status=status,priority=priority,send_at=int(time.time()))
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_noti_group(project,noti_group_id,status=9):
    sql = """select id,noti_group_id,type,content,distinct_id from {project}_noti where noti_group_id = {noti_group_id} and status = {status}""".format(project=project,noti_group_id=noti_group_id,status=status,send_at=int(time.time()))
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def select_noti_single(project,noti_id,status=9):
    sql = """select id,noti_group_id,type,content,distinct_id from {project}_noti where id = {noti_id} and status = {status}""".format(project=project,noti_id=noti_id,status=status,send_at=int(time.time()))
    result = do_tidb_select(sql=sql)
    return result[0],result[1]

def insert_noti_group(project,plan_id,list_id,data_id,temple_id,owner=None,send_at=0,sent=0,total=0,priority=13,status=8,created_at=None,updated_at=None):
    created_at=created_at if created_at else int(time.time())
    updated_at=created_at if created_at else int(time.time())
    sql = """insert {project}_noti_group (plan_id,list_id,data_id,temple_id,priority,status,owner,send_at,sent,total,created_at,updated_at ) values (%(plan_id)s,%(list_id)s,%(data_id)s,%(temple_id)s,%(priority)s,%(status)s,%(owner)s,%(send_at)s,%(sent)s,%(total)s,%(created_at)s,%(updated_at)s)""".format(project=project)
    key={'plan_id':plan_id,'list_id':list_id,'data_id':data_id,'temple_id':temple_id,'priority':priority,'status':status,'owner':owner,'send_at':send_at,'sent':sent,'total':total,'created_at':created_at if created_at else int(time.time()),'updated_at':updated_at if updated_at else int(time.time())}
    result = do_tidb_exe(sql=sql,args=key)
    return result


def insert_noti_temple(project,name,args,content,temple_desc=None):
    created_at = int(time.time())
    updated_at = int(time.time())
    sql = """insert {project}_noti_temple (name,args,temple_desc,content,created_at,updated_at ) values (%(name)s,%(args)s,%(temple_desc)s,%(content)s,%(created_at)s,%(updated_at)s)""".format(project=project)
    key={'name':name,'args':args,'temple_desc':temple_desc,'content':content,'created_at':created_at,'updated_at':updated_at}
    result = do_tidb_exe(sql=sql,args=key)
    return result

def update_noti_temple(project,temple_id,apply_times=0,lastest_apply_time=0,lastest_apply_list=0):
    updated_at = int(time.time())
    sql = """update {project}_noti_temple set apply_times=if({apply_times}=0,apply_times,apply_times+{apply_times}),lastest_apply_time=if({lastest_apply_time}=0,lastest_apply_time,{lastest_apply_time}),lastest_apply_list=if({lastest_apply_list}=0,lastest_apply_list,{lastest_apply_list}),updated_at={updated_at} where id={temple_id}""".format(project=project,temple_id=temple_id,apply_times=apply_times,lastest_apply_time=lastest_apply_time,lastest_apply_list=lastest_apply_list,updated_at=updated_at)
    result = do_tidb_exe(sql=sql)
    return result

def update_noti_group(project,noti_group_id,sent=0,total=0,status=0):
    updated_at=int(time.time())
    sql = f"""update {project}_noti_group set sent=if({sent}=0,sent,sent+1),total=if({total}=0,total,{total}),status=if({status}=0,status,{status}),updated_at={updated_at} where id={noti_group_id}"""
    result = do_tidb_exe(sql=sql)
    return result
    
def select_noti_temple(project,temple_id):
    sql= f"""select id,name,args,content from {project}_noti_temple where id={temple_id}"""
    result = do_tidb_select(sql=sql)
    return result

def select_auto_temple_apply_plan(project):
    sql = """SELECT
    {project}_usergroup_list.group_id,
    {project}_usergroup_list.id,
    {project}_usergroup_plan.func,
    {project}_usergroup_list.created_at 
FROM
    {project}_usergroup_plan
    LEFT JOIN {project}_usergroup_list ON {project}_usergroup_plan.id = {project}_usergroup_list.group_id 
WHERE
    {project}_usergroup_list.apply_temple_times = 0 
    AND {project}_usergroup_list.status = 5 
    AND {project}_usergroup_list.item_count > 0 
    AND {project}_usergroup_plan.enable_policy in (8,28) 
    AND FROM_UNIXTIME({project}_usergroup_list.list_init_date,"%Y-%m-%d") = CURRENT_DATE
ORDER BY
    {project}_usergroup_list.created_at ASC""".format(project=project)
    result = do_tidb_select(sql=sql)
    return result

def insert_usergroup_plan(project,group_title,group_desc,repeatable,priority,enable_policy,func_args):
    sql = """insert {project}_usergroup_plan (group_title,group_desc,func,repeatable,priority,enable_policy,created_at,updated_at) values (%(group_title)s,%(group_desc)s,%(func_args)s,%(repeatable)s,%(priority)s,%(enable_policy)s,%(created_at)s,%(updated_at)s)""".format(project=project)
    timenow = int(time.time())
    key={'group_title':group_title,'group_desc':group_desc,'repeatable':repeatable,'priority':priority,'enable_policy':enable_policy,'func_args':func_args,'created_at':timenow,'updated_at':timenow}
    result = do_tidb_exe(sql=sql,args=key)
    return result


def show_project_usergroup_plan(project):
    sql = f"""SELECT
	`{project}_usergroup_plan`.id as id,
	`{project}_usergroup_plan`.group_title as group_title,
	`{project}_usergroup_plan`.group_desc as group_desc,
	`{project}_usergroup_plan`.latest_data_list_index as latest_data_list_index,
	`{project}_usergroup_plan`.`repeatable` as `repeatable`,
	`{project}_usergroup_plan`.priority as priority_id,
	sc1.`desc` as priority,
	`{project}_usergroup_plan`.enable_policy as enable_policy_id,
	sc2.`desc` as enable_policy,
	`{project}_usergroup_plan`.repeat_times as repeat_times,
	from_unixtime(`{project}_usergroup_plan`.latest_data_time,"%Y-%m-%d %H:%i:%s") as latest_data_time,
	`{project}_usergroup_plan`.latest_apply_temple_id as latest_apply_temple_id,
	{project}_noti_temple.`name` as latest_apply_temple_name,
	from_unixtime(`{project}_usergroup_plan`.latest_apply_temple_time,"%Y-%m-%d %H:%i:%s") as latest_apply_temple_time,
	from_unixtime(`{project}_usergroup_plan`.created_at ,"%Y-%m-%d %H:%i:%s") as created_at,
	from_unixtime(`{project}_usergroup_plan`.updated_at,"%Y-%m-%d %H:%i:%s") as updated_at
FROM
	`{project}_usergroup_plan`
	LEFT JOIN status_code AS sc1 ON {project}_usergroup_plan.priority = sc1.id
	LEFT JOIN status_code AS sc2 ON {project}_usergroup_plan.enable_policy = sc2.id
	LEFT JOIN {project}_noti_temple ON latest_apply_temple_id = {project}_noti_temple.id
ORDER BY
	`{project}_usergroup_plan`.created_at desc"""
    # timenow = int(time.time())
    result = do_tidb_select(sql=sql)
    return result


def show_project_usergroup_list(project,plan_id):
    sql = f"""SELECT
{project}_usergroup_list.id as list_id,
{project}_usergroup_list.group_id as group_id,
{project}_usergroup_plan.group_title as group_title,
{project}_usergroup_list.group_list_index  as group_list_index,
from_unixtime(`{project}_usergroup_list`.list_init_date,"%Y-%m-%d %H:%i:%s") as list_init_date,
{project}_usergroup_list.list_desc as list_desc,
{project}_usergroup_list.jobs_id as jobs_id,
{project}_usergroup_list.item_count as item_count,
{project}_usergroup_list.`status` as status_id,
sc1.`desc` as status_name,
from_unixtime(`{project}_usergroup_list`.complete_at,"%Y-%m-%d %H:%i:%s") as complete_at,
{project}_usergroup_list.apply_temple_times as apply_temple_times,
from_unixtime(`{project}_usergroup_list`.created_at ,"%Y-%m-%d %H:%i:%s") as created_at,
from_unixtime(`{project}_usergroup_list`.updated_at,"%Y-%m-%d %H:%i:%s") as updated_at
FROM
	{project}_usergroup_list 
	LEFT JOIN {project}_usergroup_plan on {project}_usergroup_list.group_id={project}_usergroup_plan.id
	left join status_code as sc1 on {project}_usergroup_list.`status`=sc1.id
	
WHERE
	group_id = {plan_id}
	ORDER BY group_list_index desc"""
    # timenow = int(time.time())
    result = do_tidb_select(sql=sql)
    return result


def duplicate_scheduler_jobs_sql(project,list_id):
    sql=f"""insert INTO scheduler_jobs (project,
group_id,
list_index,
datetime,
`data`,
priority,
`status`,
created_at,
updated_at
) 
SELECT 
`scheduler_jobs`.project,
`scheduler_jobs`.group_id,
null,
UNIX_TIMESTAMP(CURRENT_TIME()),
`scheduler_jobs`.`data`,
`scheduler_jobs`.priority,
16,
UNIX_TIMESTAMP(CURRENT_TIME()),
UNIX_TIMESTAMP(CURRENT_TIME())
from {project}_usergroup_list join scheduler_jobs on {project}_usergroup_list.jobs_id=scheduler_jobs.id where {project}_usergroup_list.id={list_id}"""
    result = do_tidb_exe(sql=sql)
    return result

def select_usergroup_data_for_api(project,list_id,length,page,everywhere):
    #整组选择要套模板的分群
    page = (page-1)*length if page and length and page > 1 else 0
    # print(page,length)
    sql = f"""SELECT
    {project}_usergroup_list.group_id,
    {project}_usergroup_list.id,
    {project}_usergroup_data.id,
    {project}_usergroup_data.data_index,
    {project}_usergroup_data.data_key,
    {project}_usergroup_data.data_json,
    {project}_usergroup_data.`enable`,
    status_code.desc,
    {project}_usergroup_list.item_count
FROM
    {project}_usergroup_data left join {project}_usergroup_list on {project}_usergroup_data.group_list_id={project}_usergroup_list.id left join status_code on {project}_usergroup_data.`enable`=status_code.id
WHERE
    group_list_id = {list_id} {everywhere} order by  {project}_usergroup_data.data_index asc limit {page},{length}"""
    result = do_tidb_select(sql=sql)
    return result

def select_usergroup_datacount_for_api(project,list_id,length,page,everywhere):
    #整组选择要套模板的分群
    sql = f"""SELECT count(*)
FROM
    {project}_usergroup_data
WHERE
    group_list_id = {list_id} {everywhere}"""
    result = do_tidb_select(sql=sql)
    return result

def disable_usergroup_data_db(project,data_id):
    sql = f"""update {project}_usergroup_data set `enable`=10 where `id`={data_id}"""
    result = do_tidb_exe(sql=sql)
    return result

def show_temples_db(project):
    sql = f"""SELECT
	{project}_noti_temple.id,
	{project}_noti_temple.`name`,
	{project}_noti_temple.temple_desc,
	{project}_noti_temple.args,
	{project}_noti_temple.content,
	{project}_noti_temple.apply_times,
	FROM_UNIXTIME( {project}_noti_temple.lastest_apply_time, "%Y-%m-%d %H:%i:%s" ) AS lastest_apply_time,
	{project}_noti_temple.lastest_apply_list,
	{project}_usergroup_list.list_desc,
	{project}_usergroup_plan.group_title,
	FROM_UNIXTIME( {project}_noti_temple.created_at, "%Y-%m-%d %H:%i:%s" ) AS created_at,
	FROM_UNIXTIME( {project}_noti_temple.updated_at, "%Y-%m-%d %H:%i:%s" ) AS updated_at 
FROM
	`{project}_noti_temple`
	LEFT JOIN
	{project}_usergroup_list
	on {project}_noti_temple.lastest_apply_list = {project}_usergroup_list.id
	left join 
	{project}_usergroup_plan
	on {project}_usergroup_list.group_id = {project}_usergroup_plan.id order by `{project}_noti_temple`.id asc"""
    result = do_tidb_select(sql=sql)
    return result


def show_noti_group_db(project,length,page,everywhere):
    #查询推送分组列表
    page = (page-1)*length if page and length and page > 1 else 0
    sql=f"""SELECT
	{project}_noti_group.id AS noti_group_id,
	{project}_noti_group.plan_id AS plan_id,
	{project}_usergroup_plan.group_title AS plan_title,
	{project}_noti_group.list_id AS list_id,
	from_unixtime( `{project}_usergroup_list`.list_init_date, "%Y-%m-%d %H:%i:%s" ) AS list_init_date,
	{project}_usergroup_list.list_desc AS list_desc,
	{project}_usergroup_list.jobs_id AS jobs_id,
	{project}_usergroup_list.item_count AS item_count,
	{project}_usergroup_list.`status` AS list_status_id,
	lsid.`desc` as list_status,
	{project}_noti_group.data_id as data_id,
	{project}_noti_group.temple_id as temple_id,
	{project}_noti_temple.`name` as temple_name,
	{project}_noti_group.priority as priority_id,
	pid.`desc` as priority_name,
	{project}_noti_group.`status` as status_id,
	sid.`desc` as status_name,
	{project}_noti_group.owner as `owner`,
	from_unixtime( `{project}_noti_group`.send_at, "%Y-%m-%d %H:%i:%s" ) AS send_at,
	from_unixtime( `{project}_noti_group`.created_at, "%Y-%m-%d %H:%i:%s" ) AS created_at,
	from_unixtime( `{project}_noti_group`.updated_at, "%Y-%m-%d %H:%i:%s" ) AS updated_at,
	`{project}_noti_group`.sent as sent,
	`{project}_noti_group`.total as total
FROM
	`{project}_noti_group`
	LEFT JOIN {project}_usergroup_plan ON {project}_noti_group.plan_id = {project}_usergroup_plan.id
	LEFT JOIN {project}_usergroup_list ON {project}_noti_group.list_id = {project}_usergroup_list.id
	LEFT JOIN {project}_noti_temple ON {project}_noti_group.temple_id = {project}_noti_temple.id
	LEFT JOIN status_code AS pid ON {project}_noti_group.priority = pid.`id`
	LEFT JOIN status_code AS sid ON {project}_noti_group.`status` = sid.`id`
	left JOIN status_code AS lsid ON {project}_usergroup_list.`status` = lsid.id
    where 1=1 {everywhere}
    ORDER BY `{project}_noti_group`.created_at desc limit {page},{length}"""
    result = do_tidb_select(sql=sql)
    return result

def show_noti_group_count_db(project,length,page,everywhere):
    #查询推送分组列表
    page = (page-1)*length if page and length and page > 1 else 0
    sql=f"""SELECT count(*)
FROM
	`{project}_noti_group` 
    where 1=1 {everywhere}
    ORDER BY `{project}_noti_group`.created_at desc limit {page},{length}"""
    result = do_tidb_select(sql=sql)
    return result
def show_noti_db(project,length,page,everywhere):
    #查询推送分组列表
    page = (page-1)*length if page and length and page > 1 else 0
    sql=f"""SELECT
	{project}_noti.id AS noti_id,
	{project}_noti.plan_id AS plan_id,
	{project}_usergroup_plan.group_title AS plan_name,
	{project}_noti.list_id AS list_id,
	from_unixtime( `{project}_usergroup_list`.list_init_date, "%Y-%m-%d %H:%i:%s" ) AS list_init_date,
	{project}_usergroup_list.list_desc AS list_desc,
	{project}_usergroup_list.jobs_id AS jobs_id,
	lsid.`desc` as list_status,
	{project}_noti.data_id as data_id,
	{project}_noti.temple_id as temple_id,
	{project}_noti_temple.`name` as temple_name,
	{project}_noti.noti_group_id,
	{project}_noti.distinct_id,
	{project}_noti.type as type_id,
	tid.`desc` as type_name,
	{project}_noti.content,
	{project}_noti.priority as priority_id,
	pid.`desc` as priority_name,
	{project}_noti.`status` as status_id,
	sid.`desc` as status_name,
	{project}_noti.owner as `owner`,
	{project}_noti.recall_result, 
	from_unixtime( `{project}_noti`.send_at, "%Y-%m-%d %H:%i:%s" ) AS send_at,
	from_unixtime( `{project}_noti`.created_at, "%Y-%m-%d %H:%i:%s" ) AS created_at,
	from_unixtime( `{project}_noti`.updated_at, "%Y-%m-%d %H:%i:%s" ) AS updated_at
FROM
	`{project}_noti`
	LEFT JOIN {project}_usergroup_plan ON {project}_noti.plan_id = {project}_usergroup_plan.id
	LEFT JOIN {project}_usergroup_list ON {project}_noti.list_id = {project}_usergroup_list.id
	LEFT JOIN {project}_noti_temple ON {project}_noti.temple_id = {project}_noti_temple.id
	LEFT JOIN status_code AS pid ON {project}_noti.priority = pid.`id`
	LEFT JOIN status_code AS sid ON {project}_noti.`status` = sid.`id`
	left JOIN status_code AS lsid ON {project}_usergroup_list.`status` = lsid.id
	left join status_code as tid on {project}_noti.type = tid.id
    where 1=1 {everywhere}
	ORDER BY {project}_noti.created_at asc
	limit {page},{length}"""
    # print(sql)
    result = do_tidb_select(sql=sql)
    return result

def show_noti_count_db(project,length,page,everywhere):
    #查询推送分组列表
    page = (page-1)*length if page and length and page > 1 else 0
    sql=f"""SELECT count(*)
FROM
	`{project}_noti` 
    where 1=1 {everywhere}
    ORDER BY `{project}_noti`.created_at desc limit {page},{length}"""
    result = do_tidb_select(sql=sql)
    return result

def disable_noti_db(project,noti_id):
    sql=f"""update {project}_noti set `status`=10 where id={noti_id} and `status` != 26 """
    result = do_tidb_exe(sql=sql)
    return result

def show_scheduler_jobs_db(page,length):
    page = (page-1)*length if page and length and page > 1 else 0
    sql = f"""select 
    scheduler_jobs.id,
    scheduler_jobs.project,
    scheduler_jobs.group_id,
    scheduler_jobs.list_index,
    from_unixtime( scheduler_jobs.datetime, "%Y-%m-%d %H:%i:%s" ) AS start_at,
    scheduler_jobs.data,
    scheduler_jobs.priority as priority_id,
    pid.desc as priority_name,
    scheduler_jobs.status as status_id,
    sid.desc as status_name,
    from_unixtime( scheduler_jobs.created_at, "%Y-%m-%d %H:%i:%s" ) AS created_at,
    from_unixtime( scheduler_jobs.updated_at, "%Y-%m-%d %H:%i:%s" ) AS updated_at
    from scheduler_jobs 
    left join status_code as pid on scheduler_jobs.priority = pid.id
    left join status_code as sid on scheduler_jobs.`status` = sid.id
    ORDER BY scheduler_jobs.created_at desc limit {page},{length}"""
    result = do_tidb_select(sql=sql)
    return result

def show_scheduler_jobs_count_db():
    sql = f"""select count(*)
    from scheduler_jobs """
    result = do_tidb_select(sql=sql)
    return result

def insert_update_recall_blacklist(project,key,type_id,status,reason_id,latest_owner,distinct_id='',timenow=None):
    sql="""INSERT INTO `recall_blacklist` ( `project`, `distinct_id`, `key`, `type_id`, `reason_id`, `owner`, `latest_owner`, `status`, `created_at` ,`updated_at`)
VALUES
	(%(project)s,%(distinct_id)s,%(key)s,%(type_id)s,%(reason_id)s,%(owner)s,%(latest_owner)s,%(status)s,%(created_at)s,%(updated_at)s) 
	ON DUPLICATE KEY UPDATE `reason_id` =IF(%(reason_id)s != 0 ,%(reason_id)s, reason_id ),`status` =IF(%(status)s != 0,%(status)s, status ),`distinct_id` = IF(%(distinct_id)s != '',%(distinct_id)s, distinct_id ),latest_owner =%(latest_owner)s,updated_at =%(updated_at)s;"""
    timenow = int(time.time()) if not timenow else timenow
    key = {'project':project,'distinct_id':distinct_id,'key':key,'type_id':type_id,'reason_id':reason_id,'owner':latest_owner,'latest_owner':latest_owner,'status':status,'created_at':timenow,'updated_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result

def insert_recall_blacklist(project,key,type_id,status,reason_id,latest_owner,distinct_id='',timenow=None):
    sql="""INSERT INTO `recall_blacklist` ( `project`, `distinct_id`, `key`, `type_id`, `reason_id`, `owner`, `latest_owner`, `status`, `created_at` ,`updated_at`)
VALUES
	(%(project)s,%(distinct_id)s,%(key)s,%(type_id)s,%(reason_id)s,%(owner)s,%(latest_owner)s,%(status)s,%(created_at)s,%(updated_at)s);"""
    timenow = int(time.time()) if not timenow else timenow
    key = {'project':project,'distinct_id':distinct_id,'key':key,'type_id':type_id,'reason_id':reason_id,'owner':latest_owner,'latest_owner':latest_owner,'status':status,'created_at':timenow,'updated_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result

def update_recall_blacklist(project,key,type_id,status,reason_id,latest_owner,distinct_id='',timenow=None):
    sql="""UPDATE `recall_blacklist` set `reason_id` =IF(%(reason_id)s != 0 ,%(reason_id)s, reason_id ),`status` =IF(%(status)s != 0,%(status)s, status ),`distinct_id` = IF(%(distinct_id)s != '',%(distinct_id)s, distinct_id ),latest_owner =%(latest_owner)s,updated_at =%(updated_at)s where `key`=%(key)s and `type_id` = %(type_id)s and `project` = %(project)s ;"""
    timenow = int(time.time()) if not timenow else timenow
    key = {'project':project,'distinct_id':distinct_id,'key':key,'type_id':type_id,'reason_id':reason_id,'owner':latest_owner,'latest_owner':latest_owner,'status':status,'created_at':timenow,'updated_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result


def insert_recall_blacklist_reason(rbid,reason_id,reason_owner,final_status_id,reason_comment='',timenow=None):
    sql="""insert into `recall_blacklist_reason` (`rbid`,`reason_id`,`reason_owner`,`reason_comment`,`final_status_id`,`created_at`) VALUES (%(rbid)s,%(reason_id)s,%(reason_owner)s,%(reason_comment)s,%(final_status_id)s,%(created_at)s)"""
    timenow = int(time.time()) if not timenow else timenow
    key = {'rbid':rbid,'reason_id':reason_id,'reason_owner':reason_owner,'reason_comment':reason_comment,'final_status_id':final_status_id,'created_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result

def select_recall_blacklist_id(type_id,distinct_id=None,key=None,project=None,status=None,limit=None):
    add_on_status =''
    add_limit =''
    add_fliter = ''
    if limit :
        add_limit = 'limit '+str(int(limit))
    if distinct_id :
        add_fliter = add_fliter + f' and recall_blacklist.`distinct_id` = "{distinct_id}"'
    if key :
        add_fliter = add_fliter + f' and recall_blacklist.`key` = "{key}"'
    if project :
        add_fliter = add_fliter + f' and recall_blacklist.`project` = "{project}"'
    if status :
        status_int = []
        for s in status:
            status_int.append(str(int(s)))
        add_on_status = "and recall_blacklist.status in ("+",".join(status_int)+")"
    
    sql="""SELECT
	recall_blacklist.id,
	recall_blacklist.reason_id,
	r_id.`desc`,
	recall_blacklist.`owner`,
	recall_blacklist.latest_owner,
	recall_blacklist.`status`,
	s_id.`desc`,
	cast(FROM_UNIXTIME(recall_blacklist.created_at) as char),
	cast(FROM_UNIXTIME(recall_blacklist.updated_at) as char),
	recall_blacklist_reason.final_status_id,
	s2_id.`desc`,
	recall_blacklist_reason.reason_id,
	r2_id.`desc`,
	recall_blacklist_reason.reason_owner,
	recall_blacklist_reason.reason_comment,
	cast(FROM_UNIXTIME(recall_blacklist_reason.created_at) as char)
FROM
	recall_blacklist
	JOIN recall_blacklist_reason ON recall_blacklist.id = recall_blacklist_reason.rbid 
	join status_code as r_id on recall_blacklist.reason_id = r_id.id
	join status_code as s_id on recall_blacklist.`status` = s_id.id
	join status_code as r2_id on recall_blacklist_reason.`reason_id` = r2_id.id
	join status_code as s2_id on recall_blacklist_reason.`final_status_id` = s2_id.id
	where recall_blacklist.type_id = {type_id} {add_fliter} {add_on_status}
ORDER BY
	recall_blacklist_reason.created_at DESC {add_limit} ;""".format(type_id=type_id,add_fliter=add_fliter,add_on_status=add_on_status,add_limit=add_limit)
    result = do_tidb_select(sql=sql)
    return result

def select_recall_blacklist_list(type_id,distinct_id=None,project=None,status=None,start=None,limit=None):
    add_on_status =''
    add_limit =''
    add_fliter = ''
    if not start:
        start = 0
    if limit :
        add_limit = f'limit {start},{limit}'
    if distinct_id :
        add_fliter = add_fliter + f' and recall_blacklist.`distinct_id` = "{distinct_id}"'
    if project :
        add_fliter = add_fliter + f' and recall_blacklist.`project` = "{project}"'
    if status :
        status_int = []
        for s in status:
            status_int.append(str(int(s)))
        add_on_status = "and recall_blacklist.status in ("+",".join(status_int)+")"
    
    sql="""SELECT
	recall_blacklist.id,
	recall_blacklist.reason_id,
	r_id.`desc`,
	recall_blacklist.`owner`,
	recall_blacklist.latest_owner,
	recall_blacklist.`status`,
	s_id.`desc`,
	cast(FROM_UNIXTIME(recall_blacklist.created_at) as char),
	cast(FROM_UNIXTIME(recall_blacklist.updated_at) as char)
FROM
	recall_blacklist
	join status_code as r_id on recall_blacklist.`reason_id` = r_id.id
	join status_code as s_id on recall_blacklist.`status` = s_id.id
	where recall_blacklist.type_id = {type_id} {add_fliter} {add_on_status} {add_limit} ;""".format(type_id=type_id,add_fliter=add_fliter,add_on_status=add_on_status,add_limit=add_limit)
    result = do_tidb_select(sql=sql)
    return result





def insert_recall_blacklist_history(rbid,checker,result_status_id,result_reason_id,timenow=None):
    sql="""insert into `recall_blacklist_history` (`rbid`,`checker`,`result_status_id`,`result_reason_id`,`created_at`) VALUES (%(rbid)s,%(checker)s,%(result_status_id)s,%(result_reason_id)s,%(created_at)s)"""
    timenow = int(time.time()) if not timenow else timenow
    key = {'rbid':rbid,'checker':checker,'result_status_id':result_status_id,'result_reason_id':result_reason_id,'created_at':timenow}
    result = do_tidb_exe(sql=sql, args=key)
    return result