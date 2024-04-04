# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.path.append("./")
# sys.setrecursionlimt(10000000)
from component.db_op import do_tidb_select
from component.db_func import insert_devicedb,insert_user_db,find_recall_url,insert_event,find_recall_history,insert_properties,check_utm,check_distinct_id_in_device
from component.api_req import get_json_from_api
from configs import admin
import urllib.parse
import base64
import json
import traceback
from configs.export import write_to_log
from component.public_value import get_time_array_from_nlp,get_time_str
import time
import hashlib

def get_properties_value(name,data_decode):
    if '$'+name in data_decode['properties']:
        res = data_decode['properties']['$'+name]
    else:
        res = None
    return res

def get_update_content(name,decode_value):
    if decode_value != None and decode_value !='None' and decode_value !='' and decode_value != 'url的domain解析失败' and decode_value != '未取到值,直接打开' and decode_value != '未取到值_非http的url' and decode_value !='取值异常' and decode_value != 'referrer的domain解析失败' and decode_value != '未取到值':
        decode_value = decode_value
        return ',`'+name+'`='+decode_value
    else:
        return ''

def insert_user(project,data_decode,created_at=None):
    distinct_id = data_decode['distinct_id']
    lib = None
    if 'lib' in data_decode:
        if '$lib' in data_decode['lib']:
            lib = data_decode['lib']['$lib']
    elif 'properties' in data_decode:
        if '$lib' in data_decode['properties']:
            lib = data_decode['properties']['$lib']
    map_id = data_decode['map_id'] if 'map_id' in data_decode else ''
    original_id = data_decode['original_id'] if 'original_id' in data_decode else ''
    if 'userId' in data_decode['properties']:
        if data_decode['properties']['userId'] != '' and data_decode['properties']['userId']:
            user_id = data_decode['properties']['userId']
    elif 'user_id' in data_decode['properties']: 
        if data_decode['properties']['user_id'] != '' and data_decode['properties']['user_id']:
            user_id = data_decode['properties']['user_id']
    elif 'uid' in data_decode['properties']: 
        if data_decode['properties']['uid'] != '' and data_decode['properties']['uid']:
            user_id = data_decode['properties']['uid']
    else:
        user_id = None
    all_user_profile = json.dumps(data_decode['properties']) if data_decode['type'] == 'profile_set' else None 
    update_content = []
    if user_id:
        update_content.append("user_id = %(user_id)s")#.format(user_id=user_id))
    if all_user_profile:
        update_content.append("all_user_profile = %(all_user_profile)s")#.format(all_user_profile=all_user_profile))
    update_params = ''
    for item in update_content:
        #更新更新时间
        update_params = update_params + ' , ' + item
        #不更新更新时间
    try:
        insert_count = insert_user_db(project=project,distinct_id=distinct_id,lib=lib,map_id=map_id,original_id=original_id,user_id=user_id,all_user_profile=all_user_profile,update_params=update_params,created_at=created_at)
        print('插入或更新user'+str(insert_count)+'条')
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='api_tools',defname='insert_user',result=error)


def insert_device(project,data_decode,user_agent,accept_language,ip,ip_city,ip_is_good,ip_asn,ip_asn_is_good,ua_platform,ua_browser,ua_version,ua_language,created_at=None,updated_at=None):
    try:
        lib = None
        if 'lib' in data_decode:
            if '$lib' in data_decode['lib']:
                lib = data_decode['lib']['$lib']
        elif 'properties' in data_decode:
            if '$lib' in data_decode['properties']:
                lib = data_decode['properties']['$lib']
        distinct_id = data_decode['distinct_id']
        decode_values = ['device_id','manufacturer','model','os','os_version','screen_width','screen_height','network_type','is_first_day','is_first_time','wifi','app_version','carrier','referrer','referrer_host','bot_name','browser','browser_version','is_login_id','screen_orientation','latitude','longitude','utm_content','utm_campaign','utm_medium','utm_term','utm_source','latest_utm_content','latest_utm_campaign','latest_utm_medium','latest_utm_term','latest_utm_source','latest_referrer','latest_referrer_host','latest_search_keyword','latest_traffic_source_type','first_visit_time','first_referrer','first_referrer_host','first_browser_language','first_browser_charset','first_search_keyword','first_traffic_source_type']
        createVar = globals()
        for decode_value in decode_values:
            createVar[decode_value] = get_properties_value(name=decode_value,data_decode=data_decode)
        update_content=''
    #修改可能出错的空值
        if ip_is_good ==0:
            ip_city = '{}'
        elif ip_is_good ==1:
            update_content = update_content +',ip_city=%(ip_city)s'
        if ip_asn_is_good ==0:
            ip_asn = '{}'
        elif ip_asn_is_good ==1:
            update_content = update_content +',ip_asn=%(ip_asn)s'
        if wifi == True:
            wifistr = 'True'
        elif wifi == False:
            wifistr = 'False'
        else:
            wifistr = None
        if is_login_id == True:
            is_login_idstr = 'True'
        elif is_login_id == False:
            is_login_idstr = 'False'
        else:
            is_login_idstr = None
    #判断需要更新的值
        if lib !='' and lib != None:
            update_content = update_content +',lib=%(lib)s'
        if device_id !='' and device_id != None:
            update_content = update_content +',device_id=%(device_id)s'
        if ua_platform !='' and ua_platform != None:
            update_content = update_content +',ua_platform=%(ua_platform)s'
        if ua_browser !='' and ua_browser != None:
            update_content = update_content +',ua_browser=%(ua_browser)s'
        if ua_version !='' and ua_version != None:
            update_content = update_content +',ua_version=%(ua_version)s'
        if ua_language !='' and ua_language != None:
            update_content = update_content +',ua_language=%(ua_language)s'
        if manufacturer !='' and manufacturer != None:
            update_content = update_content +',manufacturer=%(manufacturer)s'
        if model !='' and model != None:
            update_content = update_content +',model=%(model)s'
        if os !='' and os != None:
            update_content = update_content +',os=%(os)s'
        if os_version !='' and os_version != None:
            update_content = update_content +',os_version=%(os_version)s'
        if screen_width !='' and screen_width != None:
            update_content = update_content +',screen_width=%(screen_width)s'
        if screen_height !='' and screen_height != None:
            update_content = update_content +',screen_height=%(screen_height)s'
        if network_type !='' and network_type != None and network_type !='NULL':
            update_content = update_content +',network_type=%(network_type)s'
        if user_agent !='' and user_agent != None:
            update_content = update_content +',user_agent=%(user_agent)s'
        if accept_language !='' and accept_language != None and accept_language !='None':
            update_content = update_content +',accept_language=%(accept_language)s'
        if ip !='' and ip != None:
            update_content = update_content +',ip=%(ip)s'
        if wifistr !='' and wifistr != None:
            update_content = update_content +',wifi=%(wifi)s'
        if app_version !='' and app_version != None:
            update_content = update_content +',app_version=%(app_version)s'
        if carrier !='' and carrier != None:
            update_content = update_content +',carrier=%(carrier)s'
        if referrer !='' and referrer != None:
            update_content = update_content +',referrer=%(referrer)s'
        if referrer_host !='' and referrer_host != None:
            update_content = update_content +',referrer_host=%(referrer_host)s'
        if bot_name !='' and bot_name != None:
            update_content = update_content +',bot_name=%(bot_name)s'
        if browser !='' and browser != None:
            update_content = update_content +',browser=%(browser)s'
        if browser_version !='' and browser_version != None:
            update_content = update_content +',browser_version=%(browser_version)s'
        if is_login_id !='' and is_login_id != None:
            update_content = update_content +',is_login_id=%(is_login_id)s'
        if screen_orientation !='' and screen_orientation != None:
            update_content = update_content +',screen_orientation=%(screen_orientation)s'
        gps_latitude = latitude
        if gps_latitude !='' and gps_latitude != None:
            update_content = update_content +',gps_latitude=%(gps_latitude)s'
        gps_longitude = longitude
        if gps_longitude !='' and gps_longitude != None:
            update_content = update_content +',gps_longitude=%(gps_longitude)s'
        if first_visit_time !='' and first_visit_time != None:
            update_content = update_content +',first_visit_time=%(first_visit_time)s'
        if first_referrer !='' and first_referrer != None and first_referrer != 'url的domain解析失败' :
            update_content = update_content +',first_referrer=%(first_referrer)s'
        if first_referrer_host !='' and first_referrer_host != None and first_referrer_host != 'url的domain解析失败':
            update_content = update_content +',first_referrer_host=%(first_referrer_host)s'
        if first_browser_language !='' and first_browser_language != None and first_browser_language != 'url的domain解析失败' and first_browser_language !='取值异常' :
            update_content = update_content +',first_browser_language=%(first_browser_language)s'
        if first_browser_charset !='' and first_browser_charset != None and first_browser_charset !='url的domain解析失败'and first_browser_charset != '取值异常':
            update_content = update_content +',first_browser_charset=%(first_browser_charset)s'
        if first_search_keyword !='' and first_search_keyword != None and first_search_keyword != '未取到值,直接打开'and first_search_keyword != '未取到值':
            update_content = update_content +',first_search_keyword=%(first_search_keyword)s'
        if first_traffic_source_type !='' and first_traffic_source_type != None:
            update_content = update_content +',first_traffic_source_type=%(first_traffic_source_type)s'
        if utm_content !='' and utm_content != None:
            update_content = update_content +',utm_content=%(utm_content)s'
        if utm_campaign !='' and utm_campaign != None:
            update_content = update_content +',utm_campaign=%(utm_campaign)s'
        if utm_medium !='' and utm_medium != None:
            update_content = update_content +',utm_medium=%(utm_medium)s'
        if utm_term !='' and utm_term != None:
            update_content = update_content +',utm_term=%(utm_term)s'
        if utm_source !='' and utm_source != None:
            update_content = update_content +',utm_source=%(utm_source)s'
        if latest_utm_content !='' and latest_utm_content != None:
            update_content = update_content +',latest_utm_content=%(latest_utm_content)s'
        if latest_utm_campaign !='' and latest_utm_campaign != None:
            update_content = update_content +',latest_utm_campaign=%(latest_utm_campaign)s'
        if latest_utm_medium !='' and latest_utm_medium != None:
            update_content = update_content +',latest_utm_medium=%(latest_utm_medium)s'
        if latest_utm_term !='' and latest_utm_term != None:
            update_content = update_content +',latest_utm_term=%(latest_utm_term)s'
        if latest_utm_source !='' and latest_utm_source != None:
            update_content = update_content +',latest_utm_source=%(latest_utm_source)s'
        if latest_referrer !='' and latest_referrer != None and latest_referrer != '取值异常' :
            update_content = update_content +',latest_referrer=%(latest_referrer)s'
        if latest_referrer_host !='' and latest_referrer_host != None and latest_referrer_host !='url的domain解析失败'    and latest_referrer_host !='取值异常' :
            update_content = update_content +',latest_referrer_host=%(latest_referrer_host)s'
        if latest_search_keyword !='' and latest_search_keyword != None and latest_search_keyword !='未取到值_直接打开' and latest_search_keyword != '未取到值' and latest_search_keyword !='url的domain解析失败'    and latest_search_keyword !='取值异常'    and latest_search_keyword != '未取到值_非http的url' :
            update_content = update_content +',latest_search_keyword=%(latest_search_keyword)s'
        if latest_traffic_source_type !='' and latest_traffic_source_type != None and latest_traffic_source_type != 'url的domain解析失败' and latest_traffic_source_type != 'referrer的domain解析失败' and latest_traffic_source_type !='取值异常':
            update_content = update_content +',latest_traffic_source_type=%(latest_traffic_source_type)s'
        count = insert_devicedb(table=project,distinct_id=distinct_id,device_id=device_id,manufacturer=manufacturer,model=model,os=os,os_version=os_version,screen_width=screen_width,screen_height=screen_height,network_type=network_type,user_agent=user_agent,accept_language=accept_language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,wifi=wifistr,app_version=app_version,carrier=carrier,referrer=referrer,referrer_host=referrer_host,bot_name=bot_name,browser=browser,browser_version=browser_version,is_login_id=is_login_idstr,screen_orientation=screen_orientation,gps_latitude=gps_latitude,gps_longitude=gps_longitude,first_visit_time=first_visit_time,first_referrer=first_referrer,first_referrer_host=first_referrer_host,first_browser_language=first_browser_language,first_browser_charset=first_browser_charset,first_search_keyword=first_search_keyword,first_traffic_source_type=first_traffic_source_type,utm_content=utm_content,utm_campaign=utm_campaign,utm_medium=utm_medium,utm_term=utm_term,utm_source=utm_source,latest_utm_content=latest_utm_content,latest_utm_campaign=latest_utm_campaign,latest_utm_medium=latest_utm_medium,latest_utm_term=latest_utm_term,latest_utm_source=latest_utm_source,latest_referrer=latest_referrer,latest_referrer_host=latest_referrer_host,latest_search_keyword=latest_search_keyword,latest_traffic_source_type=latest_traffic_source_type,update_content=update_content,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,lib=lib,created_at=created_at,updated_at=updated_at)
        print('插入或跟新device'+str(count)+'条')
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='api_tools',defname='insert_device',result=error)

def encode_urlutm(utm_source,utm_medium,utm_campaign,utm_content,utm_term):
    url_add_on = ''
    utm_list = []
    if utm_source:
        utm_list.append('utm_source='+str(urllib.parse.quote(utm_source)))
    if utm_medium:
        utm_list.append('utm_medium='+str(urllib.parse.quote(utm_medium)))
    if utm_content:
        utm_list.append('utm_content='+str(urllib.parse.quote(utm_content)))
    if utm_campaign:
        utm_list.append('utm_campaign='+str(urllib.parse.quote(utm_campaign)))
    if utm_term:
        utm_list.append('utm_term='+str(urllib.parse.quote(utm_term)))
    url_add_on = '&'.join(utm_list).replace('%23','#')
    return url_add_on

def recall_dsp(project,device_id,created_at,ids):
    history_count = find_recall_history(project=project,device_id=device_id,created_at=created_at)
    if history_count == 0 or admin.aso_dsp_callback_repeat is True:
        results,count = find_recall_url(project=project,device_id=device_id,created_at=created_at)
        for result in results:
            all_json = {}
            result_json = 'no_callback_url'
            if result[0] and result[0]!='':
                result_json = get_json_from_api(url=result[0].replace('"','').replace('{{ATYPE}}','activate').replace('{{AVALUE}}','0').replace('\\u0026','&'))
            org_distinct_id = result[2]
            all_json['src'] = json.loads(result[1])
            all_json['org_distinct_id'] = org_distinct_id
            all_json['ids'] = ids
            all_json['recall_result'] = result_json
            insert_count = insert_event(table=project,alljson=json.dumps(all_json,ensure_ascii=False),track_id=0,distinct_id=org_distinct_id.replace('"',''),lib='ghost_sa',event='$is_channel_callback_event',type_1='ghost_sa_func',User_Agent=None,Host=None,Connection=None,Pragma=None,Cache_Control=None,Accept=None,Accept_Encoding=None,Accept_Language=None,ip=None,ip_city=None,ip_asn=None,url=None,referrer=None,remark='normal',ua_platform=None,ua_browser=None,ua_version=None,ua_language=None,created_at=created_at)
            if admin.use_properties is True:
                    properties_key = []
                    for keys in all_json.keys():
                        properties_key.append(keys)
                    insert_properties(project=project,lib='ghost_sa',remark='normal',event='$is_channel_callback_event',properties=json.dumps(properties_key),properties_len=len(all_json.keys()),created_at=created_at,updated_at=created_at)
            return insert_count
    else:
        return 0


def return_dsp_utm(project,device_id,distinct_id,created_at):
    update_content = ''
    results,count = find_recall_url(project=project,device_id=device_id,created_at=created_at)
    if count > 0 :
        all_json = json.loads(results[0][1])
        his_result,his_count = check_utm(project=project,distinct_id=device_id)
        utm_content = all_json['properties']['utm_content'] if 'utm_content' in all_json['properties'] and all_json['properties']['utm_content'] != '' and all_json['properties']['utm_content'] is not None else None
        utm_campaign = all_json['properties']['utm_campaign'] if 'utm_campaign' in all_json['properties'] and all_json['properties']['utm_campaign'] != '' and all_json['properties']['utm_campaign'] is not None else None
        utm_medium = all_json['properties']['utm_medium'] if 'utm_medium' in all_json['properties'] and all_json['properties']['utm_medium'] != '' and all_json['properties']['utm_medium'] is not None else None
        utm_term = all_json['properties']['utm_term'] if 'utm_term' in all_json['properties'] and all_json['properties']['utm_term'] != '' and all_json['properties']['utm_term'] is not None else None
        utm_source = all_json['properties']['utm_source'] if 'utm_source' in all_json['properties'] and all_json['properties']['utm_source'] != '' and all_json['properties']['utm_source'] is not None else None
        utm_source = all_json['properties']['utm_source'] if 'utm_source' in all_json['properties'] and all_json['properties']['utm_source'] != '' and all_json['properties']['utm_source'] is not None else None
        src = all_json['properties']['src'] if 'src' in all_json['properties'] and all_json['properties']['src'] != '' and all_json['properties']['src'] is not None else None

        # 如果utm是空或者不存在这行，则补utm。否则更新latest_utm_content
        update_content = update_content +',latest_utm_content=%(latest_utm_content)s' if utm_content else update_content
        update_content = update_content +',utm_content=%(utm_content)s' if his_count == 0 or his_result[0][2] is None and utm_content else update_content

        update_content = update_content +',latest_utm_campaign=%(latest_utm_campaign)s' if utm_campaign else update_content
        update_content = update_content +',utm_campaign=%(utm_campaign)s' if his_count == 0 or his_result[0][3] is None and utm_campaign else update_content

        update_content = update_content +',latest_utm_medium=%(latest_utm_medium)s' if utm_medium else update_content
        update_content = update_content +',utm_medium=%(utm_medium)s' if his_count == 0 or his_result[0][4] is None and utm_medium else update_content

        update_content = update_content +',latest_utm_term=%(latest_utm_term)s' if utm_term else update_content
        update_content = update_content +',utm_term=%(utm_term)s' if his_count == 0 or his_result[0][5] is None and utm_term else update_content

        update_content = update_content +',latest_utm_source=%(latest_utm_source)s' if utm_source else update_content
        update_content = update_content +',utm_source=%(utm_source)s' if his_count == 0 or his_result[0][6] is None and utm_source else update_content

        update_content = update_content +',latest_traffic_source_type=%(latest_traffic_source_type)s' if src else update_content
        update_content = update_content +',first_traffic_source_type=%(first_traffic_source_type)s' if his_count == 0 or his_result[0][12] is None and src else update_content

        insert_device_count = insert_devicedb(table=project,distinct_id=distinct_id,device_id=device_id,manufacturer=None,model=None,os=None,os_version=None,screen_width=None,screen_height=None,network_type=None,user_agent=None,accept_language=None,ip=None,ip_city=None,ip_asn=None,wifi=None,app_version=None,carrier=None,referrer=None,referrer_host=None,bot_name=None,browser=None,browser_version=None,is_login_id=None,screen_orientation=None,gps_latitude=None,gps_longitude=None,first_visit_time=None,first_referrer=None,first_referrer_host=None,first_browser_language=None,first_browser_charset=None,first_search_keyword=None,first_traffic_source_type=src,utm_content=utm_content,utm_campaign=utm_campaign,utm_medium=utm_medium,utm_term=utm_term,utm_source=utm_source,latest_utm_content=utm_content,latest_utm_campaign=utm_campaign,latest_utm_medium=utm_medium,latest_utm_term=utm_term,latest_utm_source=utm_source,latest_referrer=None,latest_referrer_host=None,latest_search_keyword=None,latest_traffic_source_type=src,update_content=update_content,ua_platform=None,ua_browser=None,ua_version=None,ua_language=None,lib=None,created_at=created_at,updated_at=created_at)
        return insert_device_count


def gen_token():
    time_group = []
    token_group = []
    time_group.append(get_time_array_from_nlp(get_time_str(time.time()-3600)))
    time_group.append(get_time_array_from_nlp(get_time_str(time.time())))
    time_group.append(get_time_array_from_nlp(get_time_str(time.time()+3600)))
    for tokentime in time_group:
        sha1 = hashlib.sha1()
        sha1.update((admin.admin_password+tokentime['date_str']+tokentime['hour_str'][0:2]).encode(encoding='utf-8'))
        token_item = {'token':sha1.hexdigest(),'date_str':tokentime['date_str'],'hour_str':tokentime['hour_str'][0:2],'length':str(40-int(tokentime['hour_str'][0:2]))}
        token_group.append(token_item)
    return token_group


class tag_name:
    def __init__(self) -> None:
        self.tags = {}

    def check_ram(self):
        if self.tag_id in self.tags:
            return self.tags[self.tag_id]
        else:
            return None

    def update_ram(self):
        sql = f'''select `desc` from status_code where id ={self.tag_id}'''
        result  = do_tidb_select(sql=sql)
        if result[1]>0:
            self.tags[self.tag_id] = result[0][0][0]
            print('增加',self.tag_id)
        else:
            self.tags[self.tag_id] = None
            print('未找到',self.tag_id)

    def find(self,tag_id=None):
        if tag_id and tag_id !='' and tag_id !=' ' and tag_id !='""':
            self.tag_id = tag_id
            try_time = 3
            tag_name = None
            while try_time >0 and not tag_name:
                if self.check_ram():
                    return self.check_ram()
                else:
                    self.update_ram()
                try_time = try_time - 1
            return None
        else:
            return None

class user_info:
    def __init__(self) -> None:
        self.tags = {}

    def check_ram(self):
        if self.tag_id in self.tags:
            return self.tags[self.tag_id]
        else:
            return None

    def update_ram(self):
        sql = f'''select all_user_profile from {self.project}_user where distinct_id='{self.tag_id}' and all_user_profile is not null and all_user_profile != ' ' and all_user_profile != '' ORDER BY created_at desc limit 1'''
        result  = do_tidb_select(sql=sql)
        if result[1]>0:
            self.tags[self.tag_id] = json.loads(result[0][0][0])
            print('增加',self.tag_id)
        else:
            self.tags[self.tag_id] = None
            print('未找到',self.tag_id)

    def find(self,distinct_id=None,project=None):
        self.project = project
        if distinct_id and distinct_id !='' and distinct_id !=' ' and distinct_id !='""':
            self.tag_id = distinct_id
            try_time = 2
            tag_name = None
            while try_time >0 and not tag_name:
                if self.check_ram():
                    return self.check_ram()
                else:
                    self.update_ram()
                try_time = try_time - 1
            return None
        else:
            return None

class device_cache:
    #to cache device update info in ram and dump into db


    #insert_device --> check in ram -N-> check in db -N-> insert db --> sync to ram
    #check in ram --> update in ram --> check ram status -Y-> dump to db
    #                                                    -N-> next loop

    from component.public_func import show_my_memory

    def __init__(self) -> None:
        self.start_time = int(time.time())
        self.check_mem_start = int(time.time())
        self.my_memory = 0
        self.cached_data = {}
        self.request_info = ['user_agent','accept_language','ip','ip_city','ip_is_good','ip_asn','ip_asn_is_good','ua_platform','ua_browser','ua_version','ua_language','updated_at']
        self.device_properties_list = {'first':[]}
        self.device_properties_list['fix'] = ['distinct_id']
        self.device_properties_list['latest_properties'] = ['lib','device_id','manufacturer','model','os','os_version','ua_platform','ua_browser','ua_version','ua_language','screen_width','screen_height','network_type','user_agent','accept_language','ip','ip_city','ip_asn','wifi','app_version','carrier','referrer','referrer_host','bot_name','browser','browser_version','is_login_id','screen_orientation','gps_latitude','gps_longitude','latest_utm_campaign','latest_utm_medium','latest_utm_term','latest_utm_source','latest_referrer','latest_referrer_host','latest_search_keyword','latest_traffic_source_type','updated_at'],
        if admin.device_update_mode in ['first_sight','latest_sight']:
            self.device_properties_list['first'] = ['first_visit_time','first_referrer','first_referrer_host','first_browser_language','first_browser_charset','first_search_keyword','first_traffic_source_type','utm_content','utm_campaign','utm_medium','utm_term','utm_source','latest_utm_content','created_at']

    def check_mem(self):
        #check memory occupied.
        if int(time.time()-self.check_mem_start) <= admin.combine_device_max_memory_gap and self.projects != {}:
            return self.my_memory
        else:
            self.my_memory = int(self.show_my_memory())
            self.check_mem_start = int(time.time())
            return self.my_memory


    def insert_device_data(self,project,distinct_id,device_id,manufacturer,model,os,os_version,screen_width,screen_height,network_type,user_agent,accept_language,ip,ip_city,ip_asn,wifistr,app_version,carrier,referrer,referrer_host,bot_name,browser,browser_version,is_login_idstr,screen_orientation,gps_latitude,gps_longitude,first_visit_time,first_referrer,first_referrer_host,first_browser_language,first_browser_charset,first_search_keyword,first_traffic_source_type,utm_content,utm_campaign,utm_medium,utm_term,utm_source,latest_utm_content,latest_utm_campaign,latest_utm_medium,latest_utm_term,latest_utm_source,latest_referrer,latest_referrer_host,latest_search_keyword,latest_traffic_source_type,update_content,ua_platform,ua_browser,ua_version,ua_language,lib,created_at,updated_at):
        #insert data into db
        count = insert_devicedb(table=project,distinct_id=distinct_id,device_id=device_id,manufacturer=manufacturer,model=model,os=os,os_version=os_version,screen_width=screen_width,screen_height=screen_height,network_type=network_type,user_agent=user_agent,accept_language=accept_language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,wifi=wifistr,app_version=app_version,carrier=carrier,referrer=referrer,referrer_host=referrer_host,bot_name=bot_name,browser=browser,browser_version=browser_version,is_login_id=is_login_idstr,screen_orientation=screen_orientation,gps_latitude=gps_latitude,gps_longitude=gps_longitude,first_visit_time=first_visit_time,first_referrer=first_referrer,first_referrer_host=first_referrer_host,first_browser_language=first_browser_language,first_browser_charset=first_browser_charset,first_search_keyword=first_search_keyword,first_traffic_source_type=first_traffic_source_type,utm_content=utm_content,utm_campaign=utm_campaign,utm_medium=utm_medium,utm_term=utm_term,utm_source=utm_source,latest_utm_content=latest_utm_content,latest_utm_campaign=latest_utm_campaign,latest_utm_medium=latest_utm_medium,latest_utm_term=latest_utm_term,latest_utm_source=latest_utm_source,latest_referrer=latest_referrer,latest_referrer_host=latest_referrer_host,latest_search_keyword=latest_search_keyword,latest_traffic_source_type=latest_traffic_source_type,update_content=update_content,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,lib=lib,created_at=created_at,updated_at=updated_at)
        print('插入或更新device'+str(count)+'条')

    def insert_device(self,project,data_decode,user_agent,accept_language,ip,ip_city,ip_is_good,ip_asn,ip_asn_is_good,ua_platform,ua_browser,ua_version,ua_language,created_at=None,updated_at=None):
        #this is class input
        #replace insert funcion from api_tools
        insert_data_income = {'project':project,'data_decode':data_decode,'user_agent':user_agent,'accept_language':accept_language,'ip':ip,'ip_city':ip_city,'ip_asn':ip_asn,'ip_is_good':ip_is_good,'ip_asn_is_good':ip_asn_is_good,'ua_browser':ua_browser,'ua_platform':ua_platform,'ua_language':ua_language,'ua_version':ua_version,'created_at':created_at if created_at else int(time.time()),'updated_at':updated_at if created_at else int(time.time())}
        if 'distinct_id' in insert_data_income['data_decode'] and insert_data_income['data_decode']['distinct_id'] != '' and insert_data_income['project'] != '':
            #这里要求了必须有distinct_id，所以后续步骤都不需要再判断，都假定distinct_id有值。
            distinct_id = insert_data_income['data_decode']['distinct_id']
            distinct_status = self.check_distinct_id(distinct_id=distinct_id,project=insert_data_income['project'])
            #force to insert into device if there is a brand new disticnt_id
            if distinct_status == 'nowhere':
                self.insert_device_data(insert_data_income=insert_data_income)
            elif distinct_status in ('in_mem','in_device'):
                self._ram_traffic(insert_data_income=insert_data_income)
        else:
            return 'no_project_or_distinct_id'


    def check_distinct_id(self,distinct_id,project):
        if project in self.cached_data and distinct_id in self.cached_data['project']:
                #已经在缓存中，继续加缓存
                return 'in_mem'
        elif check_distinct_id_in_device(project=project,distinct_id=distinct_id) >= 1:
            #检查是否在device表里已有
            return 'in_device'
        else:
            return 'nowhere'


    def _ram_traffic(self,insert_data_income):
        #create and update pending insert data to ram data after check distinct_id is already in device table.
        if insert_data_income['project'] not in self.cached_data :
            self.cached_data[self.insert_data_income['project']] = {}
        if insert_data_income['data_decode']['distinct_id'] not in self.cached_data[insert_data_income['project']]:
            self.cached_data[insert_data_income['project']][insert_data_income['data_decode']['distinct_id']] = {}
        #if there is not distinct_id in ram,init it before update
        self.update_ram(insert_data_income=insert_data_income)
        #check throller and trans to db.
        if self.check_mem < admin.combine_device_memory :
            pass
        else:
            #dump memory
            pass


    def update_ram(self,insert_data_income):
        #判断每一个直接在request_info里带过来的原始数据
        update_value = {}
        for info_item in self.request_info:
            #当这个值有效时，再进行操作
            if info_item in insert_data_income and insert_data_income[info_item] != '':
                #当updated_at 时间小于当前缓存中的时间时，跳过单次循环，不写入更新时间，用来判断这条数据比缓存中的其他数据旧，只有需要补充字段内容的时候，才会使用这条数据。
                if info_item == 'updated_at' and 'updated_at' in self.cached_data[insert_data_income['project']][insert_data_income['data_decode']['distinct_id']] and insert_data_income[info_item] < self.cached_data[insert_data_income['project']][insert_data_income['data_decode']['distinct_id']]['updated_at']:
                    continue
                #不是updated_at的字段正常写入
                update_value[info_item]=insert_data_income[info_item]
        properties = insert_data_income['data_decode']['properties'] if 'properties' in insert_data_income['data_decode'] and insert_data_income['data_decode']['properties'] != '' else None
        #处理以新为主的数据
        for decode_item in self.device_properties_list['latest_properties']:
            if '$'+decode_item in properties and properties['$'+decode_item] != '':
                






                self.cached_data[insert_data_income['project']][insert_data_income['data_decode']['distinct_id']][info_item] = self.insert_data_income[info_item]

if info_item not in self.cached_data[insert_data_income['project']][insert_data_income['data_decode']['distinct_id']] and 



        if 'created_at' not in self.cached_data[self.insert_project][self.insert_data_decode['distinct_id']] or self.insert_data_decode['created_at'] < self.cached_data[self.insert_project][self.insert_data_decode['distinct_id']]['created_at'] :
            self.cached_data[self.insert_project][self.insert_data_decode['distinct_id']]['created_at'] = self.insert_data_decode['created_at']
        for latest in device_properties_list['latest_properties']:
            if latest not in self.cached_data





    def commit(self):
        pass

    def etl(self):
        #modify insert data to ram data
        pass



        # if 'all' not in self.projects[project]:
        #     self.projects[project]['all'] = {'ip_group':{},'ip':{},'distinct_id':{},'add_on_key':{}}
        # if event not in self.projects[project]:
        #     self.projects[project][event] = {'ip_group':{},'ip':{},'distinct_id':{},'add_on_key':{}}
        # if int(time.time())-self.start_time >= admin.access_control_max_window or self.check_mem() >= admin.access_control_max_memory:
        #     write_to_log(filename='access_control', defname='traffic', result='开始清理:'+str(self.check_mem()))
        #     self.etl()
        #     write_to_log(filename='access_control', defname='traffic', result='完成清理:'+str(self.check_mem()))
        #     self.traffic(project=project,event=event,ip_commit=ip_commit,distinct_id_commit=distinct_id_commit,add_on_key_commit=add_on_key_commit)
        # else:
        #     self.commit(project=project,event=event,ip_commit=ip_commit,distinct_id_commit=distinct_id_commit,add_on_key_commit=add_on_key_commit)
            # print('commit')
if __name__ == "__main__":
    print(gen_token())