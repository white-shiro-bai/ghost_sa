# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_func import insert_usergroup_data,insert_usergroup_list,update_usergroup_plan,check_lastest_usergroup_list_index,check_list_id
import time
import traceback
from configs.export import write_to_log
import json
import importlib
import gzip
import urllib.parse
import base64

def apply_temple(project,temple_args,temple_content,data_json,data_key,send_at=None,group_id=None,owner='system'):
    #用来把模板替换上内容（单条），当temple_args['add_on_func']['required']为真时，还会执行额外的ETL程序替换相应的内容
    func_result = None
    read_tracker = {"distinct_id": data_key,"event": "recall","lib": {"$lib": "noti"},"project": project,"properties": {"$latest_utm_campaign": "___utm_campaign___","$latest_utm_content": "___utm_content___","$latest_utm_medium": "___utm_medium___","$latest_utm_source": "___utm_source___","$latest_utm_term": "___utm_term___","$lib": "noti","_latest_utm_email": "___email___","_latest_utm_mobile": "___mobile___","action": 2,"sent_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(send_at))},"type": "track"}
    data_json['group_id'] = group_id
    if 'add_on_func' in temple_args and 'required' in temple_args['add_on_func'] and temple_args['add_on_func']['required'] is True:
        py = importlib.import_module(temple_args['add_on_func']['dir'])
        ff = getattr(py, temple_args['add_on_func']['name'])
        func_result = ff(data_json)
    for l in temple_content:
        for t in read_tracker['properties']:
            temple_content[l] = temple_content[l].replace('___owner___',owner)
            read_tracker['properties'][t] = str(read_tracker['properties'][t]).replace('___owner___',owner)
            for i in temple_args['args']:
                temple_content[l] = temple_content[l].replace('___'+i+'___',str(temple_args['args'][i]))
                read_tracker['properties'][t] = str(read_tracker['properties'][t]).replace('___'+i+'___',str(temple_args['args'][i]))
            for d in data_json:
                temple_content[l] = temple_content[l].replace('___'+d+'___',str(data_json[d])).replace('___etl_date___',time.strftime("%Y-%m-%d", time.localtime(send_at)))
                read_tracker['properties'][t] = str(read_tracker['properties'][t]).replace('___'+d+'___',str(data_json[d])).replace('___etl_date___',time.strftime("%Y-%m-%d", time.localtime(send_at)))
            if func_result:
                for k in func_result:
                    temple_content[l] = temple_content[l].replace('___'+k+'___',str(func_result[k]))
                    read_tracker['properties'][t] = str(read_tracker['properties'][t]).replace('___'+k+'___',str(func_result[k]))
    track_url = temple_args['ghost_sa']['track_url']+'?project='+project+'&data='+urllib.parse.quote(base64.b64encode((gzip.compress(json.dumps(read_tracker).encode('utf-8')))))+'&gzip=1'+('&remark='+temple_args['ghost_sa']['remark'] if 'remark' in temple_args['ghost_sa'] else '')
    temple_content["content"] = temple_content["content"].replace('___read_tracker___',track_url)
    read_tracker['properties']['action'] = 1
    temple_content["send_tracker"] = read_tracker
    temple_content["ghost_sa"] = temple_args['ghost_sa']
    return temple_content

def insert_usergroup(project,group_id,data,list_desc,jobs_id,init_time=int(time.time())):
    #重新执行该分群
    index_id = check_lastest_usergroup_list_index(project=project,group_id=group_id)
    try:
        list_init_count = insert_usergroup_list(project=project,group_id=group_id,group_index=index_id+1,status=2,list_desc=list_desc,jobs_id=jobs_id)
        list_id = check_list_id(project=project, group_id=group_id, group_list_index=index_id+1)
        data_index = 0
        for item in data['data_list']:
            data_index = data_index + 1
            if 'json' in item :
                item['json']['group_id'] = group_id
                item['json']['key'] = item['key']
            insert_usergroup_data(project=project, group_list_id=list_id[0][0], data_index=data_index, key=item['key'], json=json.dumps(item['json']), enable=item['enable'])
            insert_usergroup_list(project=project,group_id=group_id,group_index=index_id+1,list_init_date=init_time,status=3,complete_at=0,apply_temple_times=0,item_add=1,created_at=None,updated_at=None,jobs_id=jobs_id)
        insert_usergroup_list(project=project,group_id=group_id,group_index=index_id+1,status=5,complete_at=int(time.time()),jobs_id=jobs_id)
        update_usergroup_plan(project=project, plan_id=group_id, latest_data_list_index=index_id+1,updated_at=int(time.time()), repeat_times_add=1, latest_data_time=int(time.time()))
        return 5,index_id+1
    except Exception:
        error = traceback.format_exc()
        list_info = check_list_id(project=project, group_id=group_id, group_list_index=index_id+1)
        if list_info and list_info[0][1]>0:
            insert_usergroup_list(project=project,group_id=group_id,group_index=index_id+1,status=4,complete_at=int(time.time()),jobs_id=jobs_id)
            write_to_log(filename='etl_model',defname='insert_usergroup',result=error)
            return 4,index_id+1
        else :
            insert_usergroup_list(project=project,group_id=group_id,group_index=index_id+1,status=6,complete_at=int(time.time()),jobs_id=jobs_id)
            write_to_log(filename='etl_model',defname='insert_usergroup',result=error)
            return 6,0