# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import time
from component.db_func import insert_event
import json
from component.api_req import get_json_from_postjson
from component.db_op import select_tidb
from configs.export import write_to_log
import traceback

def recall_baidu_bdvid(uid, project, newType=99, convertValue=0,token="your_token_here"):
    try:
        timenow = int(time.time())
        sql_check_all_did = """select if(original_id='',distinct_id,original_id)as did from {project}_user where distinct_id='{uid}' GROUP BY did""".format(
            uid=uid, project=project)
        all_did, did_count = select_tidb(sql=sql_check_all_did)
        did_list = []
        for did in all_did:
            did_list.append("'"+did[0]+"'")
        did_str = (',').join(did_list)
        sql_find_last_bdvid = """select date,created_at,distinct_id,SUBSTRING_INDEX(SUBSTRING_INDEX(JSON_EXTRACT(all_json, '$."properties"."$url"'),'bd_vid=',-1),'"',1)as bdvid,JSON_EXTRACT(all_json, '$."properties"."$url"'),all_json from {project} where distinct_id in ({dids}) and `event`='$pageview' and JSON_EXTRACT(all_json, '$."properties"."$url"') like '%bd_vid=%' having LENGTH(bdvid)>0 ORDER BY created_at desc limit 1""".format(
            dids=did_str, project=project)
        print(sql_find_last_bdvid)
        bdvid_result, bdvid_count = select_tidb(sql=sql_find_last_bdvid)
        if bdvid_count > 0:
            latest_date = bdvid_result[0][0]
            latest_created_at = bdvid_result[0][1]
            latest_distinct_id = bdvid_result[0][2]
            latest_bdvid = bdvid_result[0][3]
            latest_url = json.loads(bdvid_result[0][4])
            jsondata = json.loads(bdvid_result[0][5])

            req_data = {"token": token,
                        "conversionTypes": [
                            {
                                "logidUrl": latest_url,
                                "newType": newType
                            }]
                        }
            if convertValue > 0:
                req_data['conversionTypes'][0]['convertValue'] = convertValue
            # print(req_data)
            json_result = get_json_from_postjson(
                url='https://ocpc.baidu.com/ocpcapi/api/uploadConvertData', data=req_data)
            all_json = {}
            all_json['req_data'] = req_data
            all_json['bdvid_result'] = jsondata
            all_json['latest_date'] = str(latest_date)
            all_json['latest_created_at'] = latest_created_at
            all_json['latest_distinct_id'] = latest_distinct_id
            all_json['latest_bdvid'] = latest_bdvid
            all_json['latest_url'] = latest_url
            all_json['recall_result'] = json_result
            all_json['all_did'] = did_list

            insert_count = insert_event(table=project, alljson=json.dumps(all_json, ensure_ascii=False), track_id=0, distinct_id=uid.replace('"', ''), lib='ghost_sa', event='$is_channel_callback_event', type_1='ghost_sa_func', User_Agent=None, Host=None, Connection=None,
                                        Pragma=None, Cache_Control=None, Accept=None, Accept_Encoding=None, Accept_Language=None, ip=None, ip_city=None, ip_asn=None, url=None, referrer=None, remark='normal', ua_platform=None, ua_browser=None, ua_version=None, ua_language=None, created_at=timenow)
            # print(all_json)
            # print(json.dumps(all_json,ensure_ascii=False))
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='sample',defname='recall_baidu_bdvid',result=sql_find_last_bdvid+error)

def recall_oceanengine_click(uid, project, event_type='active'):
    try:
        timenow = int(time.time())
        sql_check_all_did = """select if(original_id='',distinct_id,original_id)as did from {project}_user where distinct_id='{uid}' GROUP BY did""".format(
            uid=uid, project=project)
        all_did = select_tidb(sql=sql_check_all_did)
        did_list = []
        for did in all_did[0]:
            did_list.append("'"+did[0]+"'")
        did_str = (',').join(did_list)
        sql_find_last_clickid = """select date,created_at,distinct_id,SUBSTRING_INDEX(SUBSTRING_INDEX(JSON_EXTRACT(all_json, '$."properties"."$url"'),'clickid=',-1),'&creativeid=',1)as clickid,JSON_EXTRACT(all_json, '$."properties"."$url"'),all_json from {project} where distinct_id in ({dids}) and `event`='$pageview' and JSON_EXTRACT(all_json, '$."properties"."$url"') like '%clickid=%' having LENGTH(clickid)>0 ORDER BY created_at desc limit 1""".format(dids=did_str, project=project)
        print(sql_find_last_clickid)
        clickid_result = select_tidb(sql=sql_find_last_clickid)
        if clickid_result[1] > 0:
            latest_date = clickid_result[0][0][0]
            latest_created_at = clickid_result[0][0][1]
            latest_distinct_id = clickid_result[0][0][2]
            latest_clickid = clickid_result[0][0][3]
            latest_url = json.loads(clickid_result[0][0][4])
            jsondata = json.loads(clickid_result[0][0][5])
            req_data = {
                            "event_type": event_type, 
                            "context": {
                                "ad": {
                                    "callback": latest_clickid,
                                }
                            
                            },
                            "timestamp": int(time.time()*1000)
                        }
            json_result = get_json_from_postjson(
                url='https://analytics.oceanengine.com/api/v2/conversion', data=req_data)
            all_json = {}
            all_json['req_data'] = req_data
            all_json['clickid_result'] = jsondata
            all_json['latest_date'] = str(latest_date)
            all_json['latest_created_at'] = latest_created_at
            all_json['latest_distinct_id'] = latest_distinct_id
            all_json['latest_clickid'] = latest_clickid
            all_json['latest_url'] = latest_url
            all_json['recall_result'] = json_result
            all_json['all_did'] = did_list
            insert_count = insert_event(table=project, alljson=json.dumps(all_json, ensure_ascii=False), track_id=0, distinct_id=uid.replace('"', ''), lib='ghost_sa', event='$is_channel_callback_event', type_1='ghost_sa_func', User_Agent=None, Host=None, Connection=None,Pragma=None, Cache_Control=None, Accept=None, Accept_Encoding=None, Accept_Language=None, ip=None, ip_city=None, ip_asn=None, url=None, referrer=None, remark='normal', ua_platform=None, ua_browser=None, ua_version=None, ua_language=None, created_at=timenow)
    except Exception:
        error = traceback.format_exc()
        write_to_log(filename='sample',defname='recall_oceanengine_click',result=sql_find_last_clickid+error)


if __name__ == "__main__":
    recall_baidu_bdvid(uid='e4a4c6d01c742082',project='test', newType=49, convertValue=0)