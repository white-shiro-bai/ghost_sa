# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.path.append("./")
from component.db_op import do_tidb_select
from component.db_func import insert_devicedb,insert_user_db,find_recall_url,insert_event,find_recall_history,insert_properties,check_utm,check_distinct_id_in_device,update_devicedb
from component.api_req import get_json_from_api
from configs import admin
import urllib.parse
import json
import traceback
from configs.export import write_to_log
from component.public_value import get_time_array_from_nlp,get_time_str,current_timestamp10
from component.public_func import show_obj_size
import time
import hashlib
from component.url_tools import bool_to_str
from component.public_func import multi_thread_pool
from concurrent.futures import as_completed

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

    def __init__(self,combine_device_memory = admin.combine_device_memory,
                 combine_device_max_memory_gap = admin.combine_device_max_memory_gap,
                 combine_device_max_window = admin.combine_device_max_window,
                 combine_device_max_distinct_id = admin.combine_device_max_distinct_id,
                 combine_device_multiple_threads = admin.combine_device_multiple_threads,
                 use_kafka = admin.use_kafka,
                 fast_mode = admin.fast_mode,
                 unrecognized_info_skip = admin.unrecognized_info_skip,
                 device_latest_info_update_mode = admin.device_latest_info_update_mode,
                 device_source_update_mode = admin.device_source_update_mode):
        # self.start_time = int(time.time())
        self.combine_device_memory = combine_device_memory
        self.combine_device_max_memory_gap = combine_device_max_memory_gap
        self.combine_device_max_window = combine_device_max_window
        self.combine_device_max_distinct_id = combine_device_max_distinct_id
        self.combine_device_multiple_threads = combine_device_multiple_threads
        self.use_kafka = use_kafka
        self.fast_mode = fast_mode
        self.unrecognized_info_skip = unrecognized_info_skip
        self.device_latest_info_update_mode = device_latest_info_update_mode
        self.device_source_update_mode = device_source_update_mode
        self.check_mem_time = current_timestamp10()
        self.cache_size = 0
        self.cached_data = {}
        self.dump_lock = 0
        self.request_info = ['user_agent','accept_language','ip','ip_city','ip_is_good','ip_asn','ip_asn_is_good','ua_platform','ua_browser','ua_version','ua_language','created_at','updated_at']
        self.device_properties_list = {'first':[]}
        self.device_properties_list['fix'] = ['distinct_id','project']
        self.device_properties_list['latest_properties'] = ['lib','device_id','manufacturer','model','os','os_version','ua_platform','ua_browser','ua_version','ua_language','screen_width','screen_height','network_type','user_agent','accept_language','wifi','app_version','carrier','bot_name','browser','browser_version','is_login_id','screen_orientation','latitude','longitude','referrer','referrer_host','latest_utm_campaign','latest_utm_medium','latest_utm_term','latest_utm_source','latest_utm_content','latest_referrer','latest_referrer_host','latest_search_keyword','latest_traffic_source_type','updated_at']
        self.device_properties_not_str_in_restrict_mode = ['screen_width','screen_height','latitude','longitude','first_visit_time']
        if self.device_source_update_mode in ['first_sight','latest_sight']:
            self.device_properties_list['first'] = ['first_visit_time','first_referrer','first_referrer_host','first_browser_language','first_browser_charset','first_search_keyword','first_traffic_source_type','utm_content','utm_campaign','utm_medium','utm_term','utm_source','created_at']
        print('combine_device_memory:'+str(self.combine_device_memory)
        +' combine_device_max_memory_gap:'+str(self.combine_device_max_memory_gap)
        +' combine_device_max_window:'+str(self.combine_device_max_window)
        +' combine_device_max_distinct_id:'+str(self.combine_device_max_distinct_id)
        +' combine_device_multiple_threads:'+str(self.combine_device_multiple_threads)
        +' use_kafka:'+str(self.use_kafka)
        +' fast_mode:'+str(self.fast_mode)
        +' unrecognized_info_skip:'+str(self.unrecognized_info_skip)
        +' device_latest_info_update_mode:'+str(self.device_latest_info_update_mode)
        +' device_source_update_mode:'+str(self.device_source_update_mode))
        
        if self.use_kafka is False:
            write_to_log(filename='api_tools',defname='device_cache',result='当前模式为非kafka模式，由生产者写入device数据')
        elif self.use_kafka is True and self.fast_mode == 'original':
            write_to_log(filename='api_tools',defname='device_cache',result='当前模式为kakfa模式，由消费者写入按照单条方式写入数据')
        elif self.use_kafka is True and self.fast_mode == 'fast':
            write_to_log(filename='api_tools',defname='device_cache',result='当前模式为kafka模式，由消费者写入内存，再单条写入数据')
        elif self.use_kafka is True and self.fast_mode == 'boost':
            write_to_log(filename='api_tools',defname='device_cache',result='当前模式为kafka模式，由消费者写入内存，再批量写入数据，目前该模式尚未支持')

    def check_mem(self,force_check = False):
        if force_check or current_timestamp10() - self.check_mem_time > self.combine_device_max_memory_gap:
        #check memory occupied.
            self.cache_size = show_obj_size(self.cached_data)
            self.check_mem_time = current_timestamp10()
        return self.cache_size

    def _etl(self,insert_data_income):
        #insertdata to ramdate.
        #这里统一把device表不需要的空值和错值都去掉了。后续操作就不需要判断空值了
        etld = {}
        etld['project'] = insert_data_income['project']
        etld['distinct_id'] = insert_data_income['data_decode']['distinct_id']
        for info_item in self.request_info:
            if info_item in insert_data_income and insert_data_income[info_item] and insert_data_income[info_item] != '':
                etld[info_item]=insert_data_income[info_item]
        properties = insert_data_income['data_decode']['properties'] if 'properties' in insert_data_income['data_decode'] and insert_data_income['data_decode']['properties'] != '' else None
        for decode_item in self.device_properties_list['latest_properties']:
            if '$'+decode_item in properties and properties['$'+decode_item] and properties['$'+decode_item] != '':
                etld[decode_item] = properties['$'+decode_item]
        if 'lib' not in etld :
            if 'lib' in insert_data_income['data_decode'] and '$lib' in insert_data_income['data_decode']['lib'] and insert_data_income['data_decode']['lib']['$lib'] != '':
                etld['lib'] = insert_data_income['data_decode']['lib']['$lib']
        for first_item in self.device_properties_list['first']:
            if '$'+first_item in properties and properties['$'+first_item] and properties['$'+first_item] != '':
                etld[first_item] = properties['$'+first_item]
        pending_delete_key = []
        for item in etld:
            if etld[item] in self.unrecognized_info_skip:
                #剔除未识别到的值，减少更新时判断的难度，只需要判断空值即可。
                pending_delete_key.append(item)
        for item in pending_delete_key:
            del etld[item]
        if self.device_latest_info_update_mode in ['restrict']:
            #最新模式如果为严格模式，就给所有不存在的字段赋空值，防止后续因为null被更新
            for restrict_item in list(set(self.request_info).union(set(self.device_properties_list['latest_properties']))):
                if restrict_item not in etld and restrict_item not in self.device_properties_not_str_in_restrict_mode:
                    etld[restrict_item] = ''
        return etld


    def insert_device(self,project,data_decode,user_agent,accept_language,ip,ip_city,ip_is_good,ip_asn,ip_asn_is_good,ua_platform,ua_browser,ua_version,ua_language,created_at=None,updated_at=None,use_kafka=False):
        #this is class input
        #replace insert funcion from api_tools
        insert_data_income = {'project':project,'data_decode':data_decode,'user_agent':user_agent,'accept_language':accept_language,'ip':ip,'ip_city':ip_city,'ip_asn':ip_asn,'ip_is_good':ip_is_good,'ip_asn_is_good':ip_asn_is_good,'ua_browser':ua_browser,'ua_platform':ua_platform,'ua_language':ua_language,'ua_version':ua_version,'created_at':created_at if created_at else int(time.time()),'updated_at':updated_at if updated_at else int(time.time())}
        #这里要求了必须有distinct_id，所以后续步骤都不需要再判断，都假定distinct_id有值。
        if 'distinct_id' in insert_data_income['data_decode'] and insert_data_income['data_decode']['distinct_id'] != '' and insert_data_income['project'] != '':
            etld_data = self._etl(insert_data_income=insert_data_income)
            if self.fast_mode=='original' or (not self.use_kafka and not use_kafka):
                #两个都为False时，才能判断是不用kafka的模式。只有一个是False时，有可能是consumer触发的。
                self._insert_device_data(etld_data=etld_data)
            else:
                distinct_status = self.check_distinct_id(project=etld_data['project'],distinct_id=etld_data['distinct_id'])
                #force to insert into device if there is a brand new disticnt_id
                if distinct_status == 'nowhere':
                    self._insert_device_data(etld_data=etld_data)
                elif distinct_status in ('in_mem','in_device'):
                    pending =self._ram_traffic(etld_data=etld_data)
        else:
            return 'no_project_or_distinct_id'

    def _insert_device_data(self,etld_data):
        update_content = ''
        for item in etld_data:
            #这里空值不会进列表循环
            if item in ['distinct_id','project']:
                #跳过主键
                continue
            elif item == 'created_at':
                continue
            elif item == 'updated_at':
                #updated_at单独处理，只要变大就更新
                update_content = update_content +''',{item}=if(%({item})s>{item},%({item})s,{item})'''.format(item=item)
            elif item in ['latitude','longitude']:
                update_content = update_content +''',{item}=%({item})s'''.format(item='gps_'+item)
            elif 'ip_city' in etld_data and etld_data['ip_city'] != '{}' and item in ['ip_city','ip_asn','ip']:
                update_content = update_content +''',{item}=%({item})s'''.format(item=item)
            elif item in self.device_properties_list['first'] :
                if  self.device_source_update_mode in ['first_sight']:
                    #第一次模式只更新空值
                    update_content = update_content +''',{item}=if({item} is null,%({item})s,{item})'''.format(item=item)
                elif self.device_source_update_mode in ['latest_sight']:
                    #最新模式只要有值就更新
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
            elif item in self.device_properties_list['latest_properties'] :
                if  self.device_latest_info_update_mode in ['latest_sight'] and item !='':
                    #如果是最后一次模式，则只在有值时更新
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
                elif self.device_latest_info_update_mode in ['restrict']:
                    #如果是严格模式，则哪怕是空值，也会把有值的更新为空值，做到真正的严格
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
        #insert data into db
        count = insert_devicedb(table=etld_data['project'],
        distinct_id=etld_data['distinct_id'],
        device_id=etld_data['device_id'] if 'device_id' in etld_data else None,
        manufacturer=etld_data['manufacturer'] if 'manufacturer' in etld_data else None,
        model=etld_data['model'] if 'model' in etld_data else None,
        os=etld_data['os'] if 'os' in etld_data else None,
        os_version=etld_data['os_version'] if 'os_version' in etld_data else None,
        screen_width=etld_data['screen_width'] if 'screen_width' in etld_data else None,
        screen_height=etld_data['screen_height'] if 'screen_height' in etld_data else None,
        network_type=etld_data['network_type'] if 'network_type' in etld_data else None,
        user_agent=etld_data['user_agent'] if 'user_agent' in etld_data else None,
        accept_language=etld_data['accept_language'] if 'accept_language' in etld_data else None,
        ip=etld_data['ip'] if 'ip' in etld_data else None,
        ip_city=etld_data['ip_city'] if 'ip_city' in etld_data else None,
        ip_asn=etld_data['ip_asn'] if 'ip_asn' in etld_data else None,
        wifi=bool_to_str(etld_data['wifi']) if 'wifi' in etld_data else None,
        app_version=etld_data['app_version'] if 'app_version' in etld_data else None,
        carrier=etld_data['carrier'] if 'carrier' in etld_data else None,
        referrer=etld_data['referrer'] if 'referrer' in etld_data else None,
        referrer_host=etld_data['referrer_host'] if 'referrer_host' in etld_data else None,
        bot_name=etld_data['bot_name'] if 'bot_name' in etld_data else None,
        browser=etld_data['browser'] if 'browser' in etld_data else None,
        browser_version=etld_data['browser_version'] if 'browser_version' in etld_data else None,
        is_login_id=bool_to_str(etld_data['is_login_id']) if 'is_login_id' in etld_data else None,
        screen_orientation=etld_data['screen_orientation'] if 'screen_orientation' in etld_data else None,
        gps_latitude=etld_data['latitude'] if 'latitude' in etld_data else None,
        gps_longitude=etld_data['longitude'] if 'longitude' in etld_data else None,
        first_visit_time=etld_data['first_visit_time'] if 'first_visit_time' in etld_data else None,
        first_referrer=etld_data['first_referrer'] if 'first_referrer' in etld_data else None,
        first_referrer_host=etld_data['first_referrer_host'] if 'first_referrer_host' in etld_data else None,
        first_browser_language=etld_data['first_browser_language'] if 'first_browser_language' in etld_data else None,
        first_browser_charset=etld_data['first_browser_charset'] if 'first_browser_charset' in etld_data else None,
        first_search_keyword=etld_data['first_search_keyword'] if 'first_search_keyword' in etld_data else None,
        first_traffic_source_type=etld_data['first_traffic_source_type'] if 'first_traffic_source_type' in etld_data else None,
        utm_content=etld_data['utm_content'] if 'utm_content' in etld_data else None,
        utm_campaign=etld_data['utm_campaign'] if 'utm_campaign' in etld_data else None,
        utm_medium=etld_data['utm_medium'] if 'utm_medium' in etld_data else None,
        utm_term=etld_data['utm_term'] if 'utm_term' in etld_data else None,
        utm_source=etld_data['utm_source'] if 'utm_source' in etld_data else None,
        latest_utm_content=etld_data['latest_utm_content'] if 'latest_utm_content' in etld_data else None,
        latest_utm_campaign=etld_data['latest_utm_campaign'] if 'latest_utm_campaign' in etld_data else None,
        latest_utm_medium=etld_data['latest_utm_medium'] if 'latest_utm_medium' in etld_data else None,
        latest_utm_term=etld_data['latest_utm_term'] if 'latest_utm_term' in etld_data else None,
        latest_utm_source=etld_data['latest_utm_source'] if 'latest_utm_source' in etld_data else None,
        latest_referrer=etld_data['latest_referrer'] if 'latest_referrer' in etld_data else None,
        latest_referrer_host=etld_data['latest_referrer_host'] if 'latest_referrer_host' in etld_data else None,
        latest_search_keyword=etld_data['latest_search_keyword'] if 'latest_search_keyword' in etld_data else None,
        latest_traffic_source_type=etld_data['latest_traffic_source_type'] if 'latest_traffic_source_type' in etld_data else None,
        update_content=update_content,
        ua_platform=etld_data['ua_platform'] if 'ua_platform' in etld_data else None,
        ua_browser=etld_data['ua_browser'] if 'ua_browser' in etld_data else None,
        ua_version=etld_data['ua_version'] if 'ua_version' in etld_data else None,
        ua_language=etld_data['ua_language'] if 'ua_language' in etld_data else None,
        lib=etld_data['lib'] if 'lib' in etld_data else None,
        created_at=etld_data['created_at'] if 'created_at' in etld_data else None,
        updated_at=etld_data['updated_at'] if 'updated_at' in etld_data else None
        )
        print('插入或更新device'+str(count)+'条')

    def _update_device(self,project,distinct_id,data):
        # print('正在更新',project,distinct_id,data)
        update_content = ''
        for item in data:
            #这里空值不会进列表循环
            #根据配置，设定更新方式
            if item == 'created_at':
                continue
            elif item == 'updated_at':
                #updated_at单独处理，只要变大就更新
                update_content = update_content +''',{item}=if(%({item})s>{item},%({item})s,{item})'''.format(item=item)
            elif 'ip_city' in data and data['ip_city'] != '{}' and item in ['ip_city','ip_asn','ip']:
                update_content = update_content +''',{item}=%({item})s'''.format(item=item)
            elif item in ['latitude','longitude']:
                update_content = update_content +''',gps_{item}=%({item})s'''.format(item=item)
            elif item in self.device_properties_list['first'] :
                if  self.device_source_update_mode in ['first_sight']:
                    #第一次模式只更新空值
                    update_content = update_content +''',{item}=if({item} is null,%({item})s,{item})'''.format(item=item)
                elif self.device_source_update_mode in ['latest_sight']:
                    #最新模式只要有值就更新
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
            elif item in self.device_properties_list['latest_properties'] :
                if  self.device_latest_info_update_mode in ['latest_sight'] and item !='':
                    #如果是最后一次模式，则只在有值时更新
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
                elif self.device_latest_info_update_mode in ['restrict']:
                    #如果是严格模式，则哪怕是空值，也会把有值的更新为空值，做到真正的严格
                    update_content = update_content +''',{item}=%({item})s'''.format(item=item)
            #处理特殊值
            if item in ['is_login_id','wifi']:
                data[item] = bool_to_str(data[item])
        update_content = update_content.lstrip(',')
        result = update_devicedb(project=project,distinct_id=distinct_id,data=data,update_content=update_content)
        return result

    def check_distinct_id(self,distinct_id,project):
        if project in self.cached_data and distinct_id in self.cached_data[project]:
            #已经在缓存中，继续加缓存
            return 'in_mem'
        elif check_distinct_id_in_device(project=project,distinct_id=distinct_id) >= 1:
            #检查是否在device表里已有
            return 'in_device'
        else:
            return 'nowhere'


    def _ram_traffic(self,etld_data):
        #create and update pending insert data to ram data after check distinct_id is already in device table.
        if etld_data['project'] not in self.cached_data :
            self.cached_data[etld_data['project']] = {}
        if etld_data['distinct_id'] not in self.cached_data[etld_data['project']]:
            self.cached_data[etld_data['project']][etld_data['distinct_id']] = {}
        #if there is not distinct_id in ram,init it before update
        self._update_ram(etld_data=etld_data)
        #check throller and trans to db.
        # if self._check_mem() > self.combine_device_memory :
        #     dump_status = self.dump()
        #     if dump_status == 'success':
        #         self.cache_size = 0



    def _update_ram(self,etld_data):
        #判断每一个直接在request_info里带过来的原始数据
        # update_value = {}
        if ('updated_at' in self.cached_data[etld_data['project']][etld_data['distinct_id']] and self.cached_data[etld_data['project']][etld_data['distinct_id']]['updated_at'] < etld_data['updated_at'] ) or self.cached_data[etld_data['project']][etld_data['distinct_id']] == {}:
            #日期比较新的情况，处理以新为主的数据
            #处理以新为主的数据
            for info_item in self.request_info:
                if info_item not in ('created_at'):
                    self.cached_data[etld_data['project']][etld_data['distinct_id']][info_item] = etld_data[info_item]
                elif info_item in ('created_at'):
                    if info_item not in self.cached_data[etld_data['project']][etld_data['distinct_id']]:
                        self.cached_data[etld_data['project']][etld_data['distinct_id']][info_item] = etld_data[info_item]
            for decode_item in self.device_properties_list['latest_properties']:
                if decode_item in etld_data and decode_item != 'updated_at':
                    self.cached_data[etld_data['project']][etld_data['distinct_id']][decode_item] = etld_data[decode_item]
            #处理以初次为主的数据，这里只处理有的就可以，因为在init里判断了，如果是严格模式，first列表不会初始化
            for first_item in self.device_properties_list['first']:
                if first_item in etld_data and first_item not in self.cached_data[etld_data['project']][etld_data['distinct_id']]:
                    #把最后信息状态写入缓存
                    self.cached_data[etld_data['project']][etld_data['distinct_id']][first_item] = etld_data[first_item]
        else:
            #日期比较旧的情况，且最后一次的更新模式是以最后一次感知到为准，则更新。
            if self.device_latest_info_update_mode =='latest_sight':
                for latest_item in self.device_properties_list['latest_properties']:
                    if latest_item not in self.cached_data[etld_data['project']][etld_data['distinct_id']] and latest_item in etld_data:
                        #把最后信息状态写入缓存
                        self.cached_data[etld_data['project']][etld_data['distinct_id']][latest_item] = etld_data[latest_item]
            #第一次的数据，如果比现存的更早，则更新。
            if ('created_at' in etld_data and etld_data['created_at'] and 'created_at' in self.cached_data[etld_data['project']][etld_data['distinct_id']] and self.cached_data[etld_data['project']][etld_data['distinct_id']]['created_at'] > etld_data['created_at']) or self.cached_data[etld_data['project']][etld_data['distinct_id']] == {} :
                #更新created_at到更早的时间
                self.cached_data[etld_data['project']][etld_data['distinct_id']]['created_at'] = etld_data['created_at']
                for first_item in self.device_properties_list['first']:
                    if first_item in etld_data and (first_item not in self.cached_data[etld_data['project']][etld_data['distinct_id']] or self.cached_data[etld_data['project']][etld_data['distinct_id']][first_item] != etld_data[first_item]):
                        #把最后信息状态写入缓存
                        self.cached_data[etld_data['project']][etld_data['distinct_id']][first_item] = etld_data[first_item]
            #如果不比现在的更早，则根据admin.device_source_update_mode来判断是否更新。
            else:
                #如果更早拿不到数据，但仍然保持以最早感知到的为准。则更新。
                #这里判断的最早感知，是没错的。在实际数据中，大概率是发生在没有更早的有效信息了。如果是以最后感知到的为准，会在上面updated_at的环节就写入，然后在从ram-->db的过程中判断。
                if self.device_source_update_mode == 'first_sight':
                    for first_item in self.device_properties_list['first']:
                        if first_item in etld_data and first_item not in self.cached_data[etld_data['project']][etld_data['distinct_id']]:
                        #把最后信息状态写入缓存
                            self.cached_data[etld_data['project']][etld_data['distinct_id']][first_item] = etld_data[first_item]

    def dump(self):
        #dump_ram_to_db
        #dump这里执行完，不重置类的内存占用，是为了不锁定dump程序，把定时器执行时，能否由内存占用控制的权限，交给定时器。
        self.dump_lock = 1
        time.sleep(2) #置锁后，等待2秒，防止有traffic没执行完造成字典变动。
        success_count = 0 #成功更新数量
        nochange_count = 0 #相比历史无变化数量
        error = 0 #更新失败数量
        empty = 0 #仅有空对象的数量（预留以减小数据库查询压力，但最后没有数据更新）
        delete_count = 0 #删除数量
        pending_delete = {} #待删除的数据
        dump_pool = multi_thread_pool(max_workers=self.combine_device_multiple_threads, thread_name_prefix='dump_pool')
        dump_list = []
        for project in self.cached_data:
            for distinct_id in self.cached_data[project]: 
                if self.cached_data[project][distinct_id] == {}:
                    empty += 1
                    if project not in pending_delete:
                        pending_delete[project] = []
                    pending_delete[project].append(distinct_id)
                else:
                    dump_list.append({'project':project,'distinct_id':distinct_id,'data':self.cached_data[project][distinct_id]})
                    # result = self._update_device(project=project,distinct_id=distinct_id,data=self.cached_data[project][distinct_id])
        tasks = [dump_pool.submit(self._update_device, project=dump_item['project'], distinct_id=dump_item['distinct_id'], data=dump_item['data']) for dump_item in dump_list]
        for result_object in as_completed(tasks):
            result_dict  = result_object.result()
            result = result_dict['result']
            if result in ['success']:
                success_count += 1
            elif result in ['no_change']:
                nochange_count += 1
            else :
                error += 1
            if ('updated_at' in result_dict and result_dict['updated_at'] and result_dict['updated_at'] + self.combine_device_max_window < current_timestamp10() and result in ['success','no_change']) or 'updated_at' not in result_dict or not result_dict['updated_at']:
                #判断没有新数据进了再删，避免内存里找不到，去数据库里找，占用io。
                if result_dict['project'] not in pending_delete:
                    pending_delete[result_dict['project']] = []
                pending_delete[result_dict['project']].append(result_dict['distinct_id'])
        for project in pending_delete:
            for distinct_id in pending_delete[project]:
                del self.cached_data[project][distinct_id]
                delete_count += 1
        self.dump_lock = 0
        if error > 0:
            write_to_log(filename='api_tools', defname='device_cache_dump', result='success_dump:'+str(success_count)+',no_change_dump:'+str(nochange_count)+',error_dump:'+str(error)+',delete_count:'+str(delete_count),level='warning')
            return 'success with error'
        write_to_log(filename='api_tools', defname='device_cache_dump', result='success_dump:'+str(success_count)+',no_change_dump:'+str(nochange_count)+',error_dump:'+str(error)+',delete_count:'+str(delete_count),level='info')
        self.check_mem(force_check = True)
        return 'success'


device_cache_instance = device_cache()

if __name__ == "__main__":
    print(gen_token())