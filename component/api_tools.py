# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
sys.path.append("./")
# sys.setrecursionlimt(10000000)
from component.db_func import insert_devicedb,insert_user_db,find_recall_url,insert_event,find_recall_history,insert_properties,check_utm
from component.api_req import get_json_from_api
from configs import admin
import urllib.parse
import base64
import json
import traceback
from configs.export import write_to_log


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
    insert_count = insert_user_db(project=project,distinct_id=distinct_id,lib=lib,map_id=map_id,original_id=original_id,user_id=user_id,all_user_profile=all_user_profile,update_params=update_params,created_at=created_at)
    print('插入或更新user'+str(insert_count)+'条')




def insert_device(project,data_decode,user_agent,accept_language,ip,ip_city,ip_is_good,ip_asn,ip_asn_is_good,ua_platform,ua_browser,ua_version,ua_language,created_at=None,updated_at=None):
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
    if latest_referrer !='' and latest_referrer != None:
        update_content = update_content +',latest_referrer=%(latest_referrer)s'
    if latest_referrer_host !='' and latest_referrer_host != None and latest_referrer_host !='url的domain解析失败'    and latest_referrer_host !='取值异常' :
        update_content = update_content +',latest_referrer_host=%(latest_referrer_host)s'
    if latest_search_keyword !='' and latest_search_keyword != None and latest_search_keyword !='未取到值_直接打开' and latest_search_keyword != '未取到值' and latest_search_keyword !='url的domain解析失败'    and latest_search_keyword !='取值异常'    and latest_search_keyword != '未取到值_非http的url':
        update_content = update_content +',latest_search_keyword=%(latest_search_keyword)s'
    if latest_traffic_source_type !='' and latest_traffic_source_type != None and latest_traffic_source_type != 'url的domain解析失败' and latest_traffic_source_type != 'referrer的domain解析失败' and latest_traffic_source_type !='取值异常':
        update_content = update_content +',latest_traffic_source_type=%(latest_traffic_source_type)s'

    count = insert_devicedb(table=project,distinct_id=distinct_id,device_id=device_id,manufacturer=manufacturer,model=model,os=os,os_version=os_version,screen_width=screen_width,screen_height=screen_height,network_type=network_type,user_agent=user_agent,accept_language=accept_language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,wifi=wifistr,app_version=app_version,carrier=carrier,referrer=referrer,referrer_host=referrer_host,bot_name=bot_name,browser=browser,browser_version=browser_version,is_login_id=is_login_idstr,screen_orientation=screen_orientation,gps_latitude=gps_latitude,gps_longitude=gps_longitude,first_visit_time=first_visit_time,first_referrer=first_referrer,first_referrer_host=first_referrer_host,first_browser_language=first_browser_language,first_browser_charset=first_browser_charset,first_search_keyword=first_search_keyword,first_traffic_source_type=first_traffic_source_type,utm_content=utm_content,utm_campaign=utm_campaign,utm_medium=utm_medium,utm_term=utm_term,utm_source=utm_source,latest_utm_content=latest_utm_content,latest_utm_campaign=latest_utm_campaign,latest_utm_medium=latest_utm_medium,latest_utm_term=latest_utm_term,latest_utm_source=latest_utm_source,latest_referrer=latest_referrer,latest_referrer_host=latest_referrer_host,latest_search_keyword=latest_search_keyword,latest_traffic_source_type=latest_traffic_source_type,update_content=update_content,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,lib=lib,created_at=created_at,updated_at=updated_at)
    print('插入或跟新device'+str(count)+'条')

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
    url_add_on = '&'.join(utm_list)
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


if __name__ == "__main__":
        # encode_url(utm_source='测试')
        print(recall_dsp(project='fideo_v1',device_id='48D32705-BCC2-4BBC-A637-D1FFB572C96C',created_at=1592899611))