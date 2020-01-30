# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.setrecursionlimit(10000000)
import time
from component.db_op import do_tidb_exe,do_tidb_select
from configs.export import write_to_log
import traceback
# import pymysql

def insert_event(table,alljson,track_id,distinct_id,lib,event,type_1,User_Agent,Host,Connection,Pragma,Cache_Control,Accept,Accept_Encoding,Accept_Language,ip,ip_city,ip_asn,url,referrer,remark,ua_platform,ua_browser,ua_version,ua_language,created_at=None):
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
  result,count = do_tidb_exe(sql=sql, args=key)
  if count == 0:
    write_to_log(filename='db_func',defname='insert_event',result=result+sql+str(key))
  return count


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
  result,count = do_tidb_exe(sql=sql, args=key)
  return count

def insert_user_db(project,distinct_id,lib,map_id,original_id,user_id,all_user_profile,update_params,created_at=None,updated_at=None):
  if created_at is None:
    timenow = int(time.time())
    date = time.strftime("%Y-%m-%d", time.localtime())
    hour = int(time.strftime("%H", time.localtime()))
  else:
    timenow = created_at
    date = time.strftime("%Y-%m-%d", time.localtime(created_at))
    hour = int(time.strftime("%H", time.localtime(created_at)))
  all_user_profile_sql = all_user_profile
  update_params_sql = update_params
  sql = """set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 10;
  insert HIGH_PRIORITY into `{table}_user` (`distinct_id`,`lib`,`map_id`,`original_id`,`user_id`,`all_user_profile`,`created_at`,`updated_at`) values (%(distinct_id)s,%(lib)s,%(map_id)s,%(original_id)s,%(user_id)s,%(all_user_profile)s,%(created_at)s,%(updated_at)s) ON DUPLICATE KEY UPDATE `updated_at`={updated_at}{update_params}""".format(table=project,update_params=update_params_sql,updated_at=timenow)
  key={'distinct_id':distinct_id,'lib':lib,'map_id':map_id,'original_id':original_id,'user_id':user_id,'all_user_profile':all_user_profile_sql,'created_at':timenow,'updated_at':timenow}
  result,count = do_tidb_exe(sql=sql, args=key)
  return count

def check_user_device(project,distinct_id,first_id):
  #仅用于导入神策旧数据
  sql = """select first_id,second_id from users where first_id = '{first_id}'""".format(first_id=first_id)



def get_long_url_from_short(short_url):
  timenow = int(time.time())
  sql = """select HIGH_PRIORITY long_url,expired_at from shortcut where short_url ='{shorturl}' order by expired_at desc""".format(shorturl=short_url)
  result,count = do_tidb_select(sql)
  if count>0:
    long_url = result[0][0]
    expired_at  = result[0][1]
    if expired_at is None or expired_at > timenow :
      return long_url,'success'
    else:
      return '','expired'
  else:
    return '','fail'

def check_long_url(long_url):
  timenow = int(time.time())
  sql = """select project,short_url,from_unixtime(expired_at),from_unixtime(created_at),src,src_short_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term,long_url from shortcut where long_url = '{long_url}' and expired_at > {timenow}""".format(long_url=long_url,timenow=timenow)
  result,count = do_tidb_select(sql)
  if count>0:
    result_dict = []
    for item in result:
      project = result[0][0]
      short_url = result[0][1]
      expired_at = result[0][2]
      created_at = result[0][3]
      src = result[0][4]
      src_short_url = result[0][5]
      submitter = result[0][6]
      utm_source = result[0][7]
      utm_medium = result[0][8]
      utm_campaign = result[0][9]
      utm_content = result[0][10]
      utm_term = result[0][11]
      long_url = result[0][12]
      result_dict.append({'project':project,'short_url':short_url,'expired_at':expired_at,'created_at':created_at,'src':src,'src_short_url':src_short_url,'submitter':submitter,'utm_source':utm_source,'utm_medium':utm_medium,'utm_campaign':utm_campaign,'utm_content':utm_content,'utm_term':utm_term,'long_url':long_url})
    return result_dict,'exist'
  else:
    return '','empty'

def insert_shortcut(project,short_url,long_url,expired_at,src,src_short_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term):
  timenow = int(time.time())
  sql = """insert into shortcut (`project`,`short_url`,`long_url`,`expired_at`,`created_at`,`src`,`src_short_url`,`submitter`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{project}','{short_url}','{long_url}',{expired_at},{created_at},'{src}','{src_short_url}','{submitter}','{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}')""".format(project=project,short_url=short_url,long_url=long_url,expired_at=expired_at,created_at=timenow,src=src,src_short_url=src_short_url,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
    # print(sql,count)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='insert_shortcut',result=result+sql)
  return count




def show_shortcut(page,length,filters='',sort='`shortcut`.created_at',way='desc'):
  sql = """SELECT `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at,count(shortcut_history.created_at) as visit_times FROM `shortcut` left join `shortcut_history` on `shortcut`.short_url = `shortcut_history`.`short_url` {filters} GROUP BY `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at ORDER BY {sort} {way} Limit {start_pageline},{length}""".format(start_pageline=(page-1)*length,length=length,filters=filters,sort=sort,way=way)
  # print(sql)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='show_shortcut',result=str(result)+sql)
    return '',0
  return result,count

def count_shortcut(filters=''):
  sql = """SELECT count(*) FROM `shortcut` {filters} """.format(filters=filters)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='show_shortcut',result=str(result)+sql)
    return '',0
  return result


def insert_shortcut_history(short_url,result,cost_time,ip,user_agent,accept_language,ua_platform,ua_browser,ua_version,ua_language):
  timenow = int(time.time())
  sql = """insert HIGH_PRIORITY shortcut_history (`short_url`,`result`,`cost_time`,`ip`,`created_at`,`user_agent`,`accept_language`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`) values ('{short_url}','{result}',{cost_time},'{ip}',{created_at},'{user_agent}','{accept_language}','{ua_platform}','{ua_browser}','{ua_version}','{ua_language}')""".format(short_url=short_url,result=result,cost_time=cost_time,ip=ip,created_at=timenow,user_agent=user_agent,accept_language=accept_language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
  print('已插入解析记录'+str(count))



# def insert_export_user(project):
#   timenow = int(time.time())
#   sql = """insert `sa_export`.`users` (`first_id`,`second_id`,`unionid`,`id`,`all_json`,`export_at`) values ('{first_id}','{second_id}','{union_id}','{id}','{all_json}',{export_at})""".format(first_id=first_id,second_id=second_id,id=id,all_json=all_json)


def show_check(project,date,hour,order,start,limit,add_on_where):
  sql = """select distinct_id,event,type,all_json,host,user_agent,ip,url,remark,from_unixtime(created_at) from {project} where date = '{date}' and hour = {hour} {add_on_where} order by created_at {order} limit {start},{limit}""".format(project=project,date=date,hour=hour,order=order,start=start,limit=limit,add_on_where=add_on_where)
  # print(sql)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='show_check',result=str(result)+sql)
    return '',0
  return result,count