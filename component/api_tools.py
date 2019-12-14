# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("..")
# sys.setrecursionlimt(10000000)
from component.db_func import insert_devicedb,insert_user_db
import urllib.parse
import base64
import json

def get_properties_value(name,data_decode):
  if '$'+name in data_decode['properties']:
    # print(name)
    res = data_decode['properties']['$'+name]
    # print(res)
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
  # if map_id:
  #   update_content.append("map_id = %(map_id)s")#.format(map_id=map_id))
  # if original_id:
  #   update_content.append("original_id = %(original_id)s")#.format(original_id=original_id))
  if user_id:
    update_content.append("user_id = %(user_id)s")#.format(user_id=user_id))
  if all_user_profile:
    update_content.append("all_user_profile = %(all_user_profile)s")#.format(all_user_profile=all_user_profile))
  update_params = ''
  for item in update_content:
    #更新更新时间
    update_params = update_params + ' , ' + item
    #不更新更新时间
    # if len(update_params)>0:
      # update_params = update_params + ' , ' + item
    # update_params = item
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
    # print(createVar)
  #   # device_id = get_properties_value(name='device_id',data_decode=data_decode)
  # manufacturer = get_properties_value(name='manufacturer',data_decode=data_decode)
  # model = get_properties_value(name='model',data_decode=data_decode)
  # os = get_properties_value(name='os',data_decode=data_decode)
  # os_version = get_properties_value(name=os_version,data_decode=data_decode)
  # screen_width = get_properties_value(name=screen_width,data_decode=data_decode)
  # screen_height = get_properties_value(name=screen_height,data_decode=data_decode)
  # network_type = get_properties_value(name=network_type,data_decode=data_decode)
  # is_first_day = get_properties_value(name=is_first_day,data_decode=data_decode)
  # is_first_time = get_properties_value(name=is_first_time,data_decode=data_decode)
  # wifi = get_properties_value(name=wifi,data_decode=data_decode)
  # app_version = get_properties_value(name=app_version,data_decode=data_decode)
  # carrier = get_properties_value(name=carrier,data_decode=data_decode)
  # referrer = get_properties_value(name=referrer,data_decode=data_decode)
  # referrer_host = get_properties_value(name=referrer_host,data_decode=data_decode)
  # bot_name = get_properties_value(name=bot_name,data_decode=data_decode)
  # browser = get_properties_value(name=browser,data_decode=data_decode)
  # browser_version = get_properties_value(name=browser_version,data_decode=data_decode)
  # is_login_id = get_properties_value(name=is_login_id,data_decode=data_decode)
  # screen_orientation = get_properties_value(name=screen_orientation,data_decode=data_decode)
  # gps_latitude = get_properties_value(name=gps_latitude,data_decode=data_decode)
  # gps_longitude = get_properties_value(name=gps_longitude,data_decode=data_decode)
  # utm_content = get_properties_value(name=utm_content,data_decode=data_decode)
  # utm_campaign = get_properties_value(name=utm_campaign,data_decode=data_decode)
  # utm_medium = get_properties_value(name=utm_medium,data_decode=data_decode)
  # utm_term = get_properties_value(name=utm_term,data_decode=data_decode)
  # utm_source = get_properties_value(name=utm_source,data_decode=data_decode)
  # latest_utm_content = get_properties_value(name=latest_utm_content,data_decode=data_decode)
  # latest_utm_campaign = get_properties_value(name=deviclatest_utm_campaigne_id,data_decode=data_decode)
  # latest_utm_medium = get_properties_value(name=latest_utm_medium,data_decode=data_decode)
  # latest_utm_term = get_properties_value(name=latest_utm_term,data_decode=data_decode)
  # latest_utm_source = get_properties_value(name=latest_utm_source,data_decode=data_decode)
  # latest_referrer = get_properties_value(name=latest_referrer,data_decode=data_decode)
  # latest_referrer_host = get_properties_value(name=latest_referrer_host,data_decode=data_decode)
  # latest_search_keyword = get_properties_value(name=latest_search_keyword,data_decode=data_decode)
  # latest_traffic_source_type = get_properties_value(name=latest_traffic_source_type,data_decode=data_decode)
  # first_visit_time = get_properties_value(name=first_visit_time,data_decode=data_decode)
  # first_referrer = get_properties_value(name=first_referrer,data_decode=data_decode)
  # first_referrer_host = get_properties_value(name=first_referrer_host,data_decode=data_decode)
  # first_browser_language = get_properties_value(name=first_browser_language,data_decode=data_decode)
  # first_browser_charset = get_properties_value(name=first_browser_charset,data_decode=data_decode)
  # first_search_keyword = get_properties_value(name=first_search_keyword,data_decode=data_decode)
  # first_traffic_source_type = get_properties_value(name=first_traffic_source_type,data_decode=data_decode)
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
  if latest_referrer_host !='' and latest_referrer_host != None and latest_referrer_host !='url的domain解析失败'  and latest_referrer_host !='取值异常' :
    update_content = update_content +',latest_referrer_host=%(latest_referrer_host)s'
  if latest_search_keyword !='' and latest_search_keyword != None and latest_search_keyword !='未取到值_直接打开' and latest_search_keyword != '未取到值' and latest_search_keyword !='url的domain解析失败'  and latest_search_keyword !='取值异常'  and latest_search_keyword != '未取到值_非http的url':
    update_content = update_content +',latest_search_keyword=%(latest_search_keyword)s'
  if latest_traffic_source_type !='' and latest_traffic_source_type != None and latest_traffic_source_type != 'url的domain解析失败' and latest_traffic_source_type != 'referrer的domain解析失败' and latest_traffic_source_type !='取值异常':
    update_content = update_content +',latest_traffic_source_type=%(latest_traffic_source_type)s'

  count = insert_devicedb(table=project,distinct_id=distinct_id,device_id=device_id,manufacturer=manufacturer,model=model,os=os,os_version=os_version,screen_width=screen_width,screen_height=screen_height,network_type=network_type,user_agent=user_agent,accept_language=accept_language,ip=ip,ip_city=ip_city,ip_asn=ip_asn,wifi=wifistr,app_version=app_version,carrier=carrier,referrer=referrer,referrer_host=referrer_host,bot_name=bot_name,browser=browser,browser_version=browser_version,is_login_id=is_login_idstr,screen_orientation=screen_orientation,gps_latitude=gps_latitude,gps_longitude=gps_longitude,first_visit_time=first_visit_time,first_referrer=first_referrer,first_referrer_host=first_referrer_host,first_browser_language=first_browser_language,first_browser_charset=first_browser_charset,first_search_keyword=first_search_keyword,first_traffic_source_type=first_traffic_source_type,utm_content=utm_content,utm_campaign=utm_campaign,utm_medium=utm_medium,utm_term=utm_term,utm_source=utm_source,latest_utm_content=latest_utm_content,latest_utm_campaign=latest_utm_campaign,latest_utm_medium=latest_utm_medium,latest_utm_term=latest_utm_term,latest_utm_source=latest_utm_source,latest_referrer=latest_referrer,latest_referrer_host=latest_referrer_host,latest_search_keyword=latest_search_keyword,latest_traffic_source_type=latest_traffic_source_type,update_content=update_content,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language=ua_language,lib=lib,created_at=created_at,updated_at=updated_at)
  print('插入或跟新device'+str(count)+'条')

def encode_urlutm(utm_source,utm_medium,utm_campaign,utm_content,utm_term):
  url_add_on = ''
  if utm_source:
    url_add_on = url_add_on+'utm_source='+str(urllib.parse.quote(utm_source))+'&'
  if utm_medium:
    url_add_on = url_add_on+'utm_medium='+str(urllib.parse.quote(utm_medium))+'&'
  if utm_content:
    url_add_on = url_add_on+'utm_content='+str(urllib.parse.quote(utm_content))+'&'
  if utm_campaign:
    url_add_on = url_add_on+'utm_campaign='+str(urllib.parse.quote(utm_campaign))+'&'
  if utm_term:
    url_add_on = url_add_on+'utm_term='+str(urllib.parse.quote(utm_term))+'&'
  return url_add_on

if __name__ == "__main__":
    encode_url(utm_source='测试')