# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.path.append("./")
# sys.setrecursionlimt(10000000)
from app.component.db_func import insert_devicedb,insert_user_db,find_recall_url,insert_event,find_recall_history,insert_properties,check_utm
from app.component.api_req import get_json_from_api
from app.configs import admin
import urllib.parse
import base64
import json
import traceback
from app.configs.export import write_to_log
from app.component.public_value import get_time_array_from_nlp,get_time_str
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


if __name__ == "__main__":
    print(gen_token())