# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.setrecursionlimit(10000000)
import time
from component.db_op import do_tidb_exe,do_tidb_select
from configs.export import write_to_log
from configs import admin
import traceback

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

def insert_properties(project,lib,remark,event,properties,properties_len,created_at=None,updated_at=None):
  if created_at is None:
    created_at = int(time.time())
  if updated_at is None:
    updated_at = int(time.time())
  sql = """set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 10;
  insert HIGH_PRIORITY into `{table}_properties` (`lib`,`remark`,`event`,`properties`,`properties_len`,`created_at`,`updated_at`,`total_count`,`lastinsert_at`) values ( %(lib)s,%(remark)s,%(event)s,%(properties)s,%(properties_len)s,%(created_at)s,%(updated_at)s,1,%(updated_at)s) ON DUPLICATE KEY UPDATE `properties`=if(properties_len<%(properties_len)s,%(properties)s,properties),`properties_len`=if(properties_len<%(properties_len)s,%(properties_len)s,properties_len),updated_at=if(properties_len<%(properties_len)s,%(updated_at)s,updated_at),total_count=total_count+1,lastinsert_at=%(updated_at)s;""".format(table=project)
  key = {'lib':lib,'remark':remark,'event':event,'properties':properties,'properties_len':properties_len,'created_at':created_at,'updated_at':updated_at}
  result,count = do_tidb_exe(sql=sql, args=key)

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
  sql = """SELECT `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at,count(shortcut_history.created_at) as visit_times,count(shortcut_read.created_at) as read_times FROM `shortcut` left join `shortcut_history` on `shortcut`.short_url = `shortcut_history`.`short_url`  left join `shortcut_read` on `shortcut`.short_url = `shortcut_read`.`short_url` {filters} GROUP BY `shortcut`.project,`shortcut`.short_url,`shortcut`.long_url,from_unixtime(`shortcut`.expired_at),from_unixtime(`shortcut`.created_at),`shortcut`.src,`shortcut`.src_short_url,`shortcut`.submitter,`shortcut`.utm_source,`shortcut`.utm_medium,`shortcut`.utm_campaign,`shortcut`.utm_content,`shortcut`.utm_term,shortcut.created_at,shortcut.expired_at ORDER BY {sort} {way} Limit {start_pageline},{length}""".format(start_pageline=(page-1)*length,length=length,filters=filters,sort=sort,way=way)
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


def insert_shortcut_history(short_url,result,cost_time,ip,user_agent,accept_language,ua_platform,ua_browser,ua_version,ua_language,created_at=None):
  timenow = int(time.time())
  sql = """insert HIGH_PRIORITY shortcut_history (`short_url`,`result`,`cost_time`,`ip`,`created_at`,`user_agent`,`accept_language`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`) values ('{short_url}','{result}',{cost_time},'{ip}',{created_at},'{user_agent}','{accept_language}','{ua_platform}','{ua_browser}','{ua_version}','{ua_language}')""".format(short_url=short_url,result=result,cost_time=cost_time,ip=ip,created_at= created_at if created_at else timenow,user_agent=user_agent,accept_language=accept_language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
  print('已插入解析记录'+str(count))


def show_check(project,date,hour,order,start,limit,add_on_where):
  sql = """select distinct_id,event,type,all_json,host,user_agent,ip,url,remark,from_unixtime(created_at) from {project} where date = '{date}' and hour = {hour} {add_on_where} order by created_at {order} limit {start},{limit}""".format(project=project,date=date,hour=hour,order=order,start=start,limit=limit,add_on_where=add_on_where)
  # print(sql)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='show_check',result=str(result)+sql)
    return '',0
  return result,count

def show_project():
  sql = """select project_name,FROM_UNIXTIME(created_at),FROM_UNIXTIME(expired_at) from project_list order by project_name"""
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='show_project',result=str(result)+sql)
    return '',0
  return result,count

def insert_mobile_ad_src(src,src_name,src_args,utm_source,utm_medium,utm_campaign,utm_content,utm_term):
  timenow = int(time.time())
  sql = """insert mobile_ad_src (`src`,`src_name`,`src_args`,`created_at`,`updated_at`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{src}','{src_name}','{src_args}',{created_at},{updated_at},'{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}') ON DUPLICATE KEY UPDATE `src_name`='{src_name}',`src_args`='{src_args}',`updated_at`={updated_at},`utm_source`='{utm_source}',`utm_medium`='{utm_medium}',`utm_campaign`='{utm_campaign}',`utm_content`='{utm_content}',`utm_term`='{utm_term}' """.format(src=src,src_name=src_name,src_args=src_args,created_at=timenow,updated_at=timenow,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='insert_mobile_ad_src',result=str(result)+sql)
    return '',0
  return result,count



def insert_mobile_ad_list(project,url,src,src_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term,expired_at=2147483647):
  timenow = int(time.time())
  sql="""insert mobile_ad_list (`project`,`url`,`expired_at`,`created_at`,`src`,`src_url`,`submitter`,`utm_source`,`utm_medium`,`utm_campaign`,`utm_content`,`utm_term`) values ('{project}','{url}',{expired_at},{created_at},'{src}','{src_url}','{submitter}','{utm_source}','{utm_medium}','{utm_campaign}','{utm_content}','{utm_term}')""".format(project=project,url=url,expired_at=expired_at,created_at=timenow,src=src,src_url=src_url,submitter=submitter,utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,utm_term=utm_term).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='insert_mobile_ad_list',result=str(result)+sql)
    return '',0
  return result,count

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
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='read_mobile_ad_list',result=str(result)+sql)
    return '',0
  return result,count


def count_mobile_ad_list(filters=''):
  sql = """SELECT count(*) FROM `mobile_ad_list` {filters} """.format(filters=filters)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='count_mobile_ad_list',result=str(result)+sql)
    return '',0
  return result

def read_mobile_ad_src_list(add_on_where=''):
  timenow = int(time.time())
  sql = """select src,src_name,src_args,from_unixtime(created_at),from_unixtime(updated_at),if({timenow}-created_at<=604800,1,0),utm_source,utm_medium,utm_campaign,utm_content,utm_term from mobile_ad_src {add_on_where} order by src_name""".format(add_on_where=add_on_where,timenow=timenow)
  result,count = do_tidb_select(sql)
  if count == 0:
    # print(result,sql)
    write_to_log(filename='db_func',defname='read_mobile_ad_src_list',result=str(result)+sql)
    return '',0
  return result,count

def check_mobile_ad_url(url):
  timenow = int(time.time())
  sql = """select project,url,from_unixtime(expired_at),from_unixtime(created_at),src,src_url,submitter,utm_source,utm_medium,utm_campaign,utm_content,utm_term from mobile_ad_list where url = '{url}' and expired_at > {timenow}""".format(url=url,timenow=timenow)
  result,count = do_tidb_select(sql)
  if count>0:
    result_dict = []
    for item in result:
      result_dict.append({'project':item[0],'url':item[1],'expired_at':item[2],'created_at':item[3],'src':item[4],'src_url':item[5],'submitter':item[6],'utm_source':item[7],'utm_medium':item[8],'utm_campaign':item[9],'utm_content':item[10],'utm_term':item[11]})
    return result_dict,'exist'
  else:
    return '','empty'

def distinct_id_query(distinct_id,project):
  sql = """SELECT 1 FROM {project} where distinct_id ='{distinct_id}' limit 1""".format(distinct_id=distinct_id,project=project)
  result,count = do_tidb_select(sql)
  return count

def find_recall_url(project,device_id,created_at):
  date = time.strftime("%Y-%m-%d", time.localtime(created_at))
  sql = """select JSON_EXTRACT(all_json,'$."properties"."callback_url"'),all_json,distinct_id from {project} where date >= DATE_SUB('{date}',INTERVAL {day_diff} day) and date <= '{date}' and `event` = '$AppChannelMatching' and distinct_id in ('{device_id}',md5('{device_id}'),replace('{device_id}','"',''),md5(replace('{device_id}','"',''))) order by created_at desc limit 1""".format(project=project,device_id=device_id,date=date,day_diff=admin.aso_dsp_callback_interval_days)
  result,count = do_tidb_select(sql)
  return result,count

def find_recall_history(project,device_id,created_at):
  date = time.strftime("%Y-%m-%d", time.localtime(created_at))
  sql = """select count(1) from {project} where date >= DATE_SUB('{date}',INTERVAL {day_diff}  day) and date <= '{date}' and `event` = '$is_channel_callback_event' and distinct_id in ('{device_id}',md5('{device_id}'),replace('{device_id}','"',''),md5(replace('{device_id}','"','')))""".format(project=project,device_id=device_id,date=date,day_diff=admin.aso_dsp_callback_interval_days)
  result,count = do_tidb_select(sql)
  return result[0][0]

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
  result,count = do_tidb_select(sql)
  return result,count


def insert_shortcut_read(short_url,ip,user_agent,accept_language,ua_platform,ua_browser,ua_version,ua_language,referrer,created_at=None):
  timenow = int(time.time())
  sql = """insert HIGH_PRIORITY shortcut_read (`short_url`,`ip`,`created_at`,`user_agent`,`accept_language`,`ua_platform`,`ua_browser`,`ua_version`,`ua_language`,`referrer`) values ('{short_url}','{ip}',{created_at},'{user_agent}','{accept_language}','{ua_platform}','{ua_browser}','{ua_version}','{ua_language}','{referrer}')""".format(short_url=short_url,ip=ip,created_at=created_at if created_at else timenow,user_agent=user_agent,accept_language=accept_language,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,referrer=referrer).replace("'None'","Null").replace("None","Null")
  result,count = do_tidb_exe(sql)
  print('已插入解析记录'+str(count))