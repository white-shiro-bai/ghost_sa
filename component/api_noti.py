# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.url_tools import get_url_params
from configs.export import write_to_log
from configs import admin
from component.public_value import get_next_time
import time
from flask import request,jsonify,Response,redirect
import traceback
from component.db_func import show_project_usergroup_plan,show_project_usergroup_list,duplicate_scheduler_jobs_sql,select_usergroup_data_for_api,select_usergroup_datacount_for_api,disable_usergroup_data_db,show_temples_db,show_noti_group_db,show_noti_group_count_db,show_noti_db,show_noti_count_db,select_noti_group,select_noti_single,disable_noti_db,show_scheduler_jobs_db,show_scheduler_jobs_count_db,select_usergroup_jobs_plan_manual,insert_scheduler_job,select_noti_temple
import json
from scheduler import create_noti_group
from component.messenger import send_manual,create_non_usergroup_noti,create_non_usergroup_non_temple_noti
from scheduler_jobs.etl_model import apply_temple



def show_usergroup_plan():
    #查询用户分群计划列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    mode = get_url_params('mode')
    if password == admin.admin_password and project and request.method == 'POST':#只有正确的密码才能触发动作
        # remark = request.form.get('remark',None)k+'\''
        try:
            results= show_project_usergroup_plan(project=project)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                     temp_json.append({"plan_id":item[0],"group_title":item[1],"latest_data_list_index":item[3],"repeatable":item[4],"priority":item[6],"enable_policy":item[8],"repeat_times":item[9],"latest_data_time":item[10],"latest_apply_temple_name":item[12],"latest_apply_temple_time":item[13],"updated_at":item[15]})
                else:
                    temp_json.append({"plan_id":item[0],"group_title":item[1],"group_desc":item[2],"latest_data_list_index":item[3],"repeatable":item[4],"priority_id":item[5],"priority":item[6],"enable_policy_id":item[7],"enable_policy":item[8],"repeat_times":item[9],"latest_data_time":item[10],"latest_apply_temple_id":item[11],"latest_apply_temple_name":item[12],"latest_apply_temple_time":item[13],"created_at":item[14],"updated_at":item[15]})
            time_cost = round(time.time() - start_time,2)
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_usergroup_plan',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)
    # return jsonify('少参数')        # return 


def show_usergroup_list():
    #查询计划下的用户分群列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    plan_id = get_url_params('plan_id')
    mode = get_url_params('mode')
    if password == admin.admin_password and project and request.method == 'POST' and plan_id:#只有正确的密码才能触发动作
        # remark = request.form.get('remark',None)k+'\''
        try:
            results= show_project_usergroup_list(project=project,plan_id=plan_id)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                    temp_json.append({"list_id":item[0],"group_id":item[1],"group_title":item[2],"group_list_index":item[3],"list_init_date":item[4],"list_desc":item[5],"jobs_id":item[6],"item_count":item[7],"status_name":item[9],"complete_at":item[10],"apply_temple_times":item[11],"created_at":item[12],"updated_at":item[13]})
                else:
                    temp_json.append({"list_id":item[0],"group_id":item[1],"group_title":item[2],"group_list_index":item[3],"list_init_date":item[4],"list_desc":item[5],"jobs_id":item[6],"item_count":item[7],"status_id":item[8],"status_name":item[9],"complete_at":item[10],"apply_temple_times":item[11],"created_at":item[12],"updated_at":item[13]})
            
            time_cost = round(time.time() - start_time,2)
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_usergroup_list',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)
    # return jsonify('少参数')        # return 


def duplicate_scheduler_jobs():
    #重新执行分群
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    list_id = get_url_params('list_id')
    if password == admin.admin_password and project and request.method == 'POST' and list_id:#只有正确的密码才能触发动作
        # remark = request.form.get('remark',None)k+'\''
        try:
            results = duplicate_scheduler_jobs_sql(project=project,list_id=list_id)
            temp_json = []
            time_cost = round(time.time() - start_time,2)
            if results[1]>0:
                returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,"added_id":results[2]}
            else:
                returnjson = {'result':'fail','results_count':results[1],'timecost':time_cost,'data':temp_json,"error":"该列表不是由系统创建的，不支持重做"}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='duplicate_scheduler_jobs',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)
    # return jsonify('少参数')        # return 

def show_usergroup_data():
    #查询分群内容
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    list_id = get_url_params('list_id')
    length = get_url_params('length')
    page = get_url_params('page')
    everywhere = get_url_params('everywhere')
    length = int(length) if length else 500
    page = int(page) if page else 1

    if password == admin.admin_password and project and request.method == 'POST' and list_id:#只有正确的密码才能触发动作
        add_on_where = f'''and concat({project}_usergroup_data.data_key,{project}_usergroup_data.data_json) like "%{everywhere}%"''' if everywhere and everywhere !='' and everywhere != ' ' else ''
        try:
            results = select_usergroup_data_for_api(project=project,list_id=list_id,length=length,page=page,everywhere=add_on_where)
            resultscount = select_usergroup_datacount_for_api(project=project,list_id=list_id,length=length,page=page,everywhere=add_on_where)
            temp_json = []
            for item in results[0]:
                temp_json.append({"group_id":item[0],"list_id":item[1],"data_id":item[2],"data_index":item[3],"data_key":item[4],"data_json":json.loads(item[5]),"enable_policy_id":item[6],"enable_policy_name":item[7]})
            time_cost = round(time.time() - start_time,2)
            total_count = resultscount[0][0][0] if resultscount[1] > 0 else 0
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,'total_count':total_count,'page':page,'length':length}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_usergroup_data',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def disable_usergroup_data():
    #禁用单条分群数据
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    data_id = get_url_params('data_id')
    if password == admin.admin_password and project and request.method == 'POST' and data_id:#只有正确的密码才能触发动作
        # remark = request.form.get('remark',None)k+'\''
        try:
            results = disable_usergroup_data_db(project=project,data_id=data_id)
            temp_json = []
            time_cost = round(time.time() - start_time,2)
            if results[1]>0:
                returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,"disable_data_id":data_id}
            else:
                returnjson = {'result':'fail','results_count':results[1],'timecost':time_cost,'data':temp_json,"error":"没有修改任何内容"}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='disable_usergroup_data',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def show_temples():
    #查询模板列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    mode = get_url_params('mode')
    if password == admin.admin_password and project and request.method == 'POST':#只有正确的密码才能触发动作
        # remark = request.form.get('remark',None)k+'\''
        try:
            results= show_temples_db(project=project)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                    temp_json.append({"temple_id":item[0],"temple_name":item[1],"temple_desc":item[2],"apply_times":item[5],"lastest_apply_time":item[6],"lastest_apply_list_desc":item[8],"lastest_apply_group_name":item[9],"created_at":item[10],"updated_at":item[11]})
                else:
                    temp_json.append({"temple_id":item[0],"temple_name":item[1],"temple_desc":item[2],"temple_args":json.loads(item[3]),"temple_content":json.loads(item[4]),"apply_times":item[5],"lastest_apply_time":item[6],"lastest_apply_list_id":item[7],"lastest_apply_list_desc":item[8],"lastest_apply_group_name":item[9],"created_at":item[10],"updated_at":item[11]})
            
            time_cost = round(time.time() - start_time,2)
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_temples',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def apply_temples_list():
    #应用模板到分群列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    temple_id = get_url_params('temple_id')
    user_group_id = get_url_params('user_group_id')
    data_id = get_url_params('data_id')
    owner = get_url_params('owner')
    send_at = get_url_params('send_at')
    send_at = int(send_at) if send_at else int(time.time())
    if password == admin.admin_password and project and owner and request.method == 'POST':#只有正确的密码才能触发动作
        try:
            results = create_noti_group(project=project,temple_id=temple_id,user_group_id=user_group_id,data_id=data_id,owner=owner,send_at=send_at) #实际开始应用模板（单条数据和分群列表同时存在时，使用单条数据）
            temp_json = []
            time_cost = round(time.time() - start_time,2)
            returnjson = {'result':results,'timecost':time_cost,'data':temp_json}
            # print(returnjson)
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='apply_temples_list',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def show_noti_group():
        #查询推送列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    length = get_url_params('length')
    plan_id = get_url_params('plan_id')
    list_id = get_url_params('list_id')
    temple_id = get_url_params('temple_id')
    page = get_url_params('page')
    owner = get_url_params('owner')
    ngid = get_url_params('id')
    mode = get_url_params('mode')
    length = int(length) if length else 50
    page = int(page) if page else 1

    if password == admin.admin_password and project and request.method == 'POST':
        #只有正确的密码才能触发动作
        add_on_where = ''
        add_on_where = add_on_where +(''' and {project}_noti_group.plan_id = {plan_id}'''.format(project=project,plan_id=int(plan_id)) if plan_id and plan_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti_group.list_id = {list_id}'''.format(project=project,list_id=int(list_id)) if list_id and list_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti_group.temple_id = {temple_id}'''.format(project=project,temple_id=int(temple_id)) if temple_id and temple_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti_group.id = {ngid}'''.format(project=project,ngid=int(ngid)) if ngid and ngid !='' else '')
        if not mode or mode != 'cli' :
            add_on_where = add_on_where +(f''' and {project}_noti_group.owner like "%{owner}%"''' if owner and owner !='' else '')
        try:
            results = show_noti_group_db(project=project,length=length,page=page,everywhere=add_on_where)
            resultscount = show_noti_group_count_db(project=project,length=length,page=page,everywhere=add_on_where)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                    temp_json.append({"noti_group_id":item[0],"plan_title":item[2],"list_id":item[3],"list_init_date":item[4],"list_desc":item[5],"jobs_id":item[6],"item_count":item[7],"list_status":item[9],"temple_name":item[12],"priority_name":item[14],"status_name":item[16],"owner":item[17],"send_at":item[18],"created_at":item[19],"updated_at":item[20],"sent_success":str(item[21])+"/"+str(item[22])})
                else:
                    temp_json.append({"noti_group_id":item[0],"plan_id":item[1],"plan_title":item[2],"list_id":item[3],"list_init_date":item[4],"list_desc":item[5],"jobs_id":item[6],"item_count":item[7],"list_status_id":item[8],"list_status":item[9],"data_id":item[10],"temple_id":item[11],"temple_name":item[12],"priority_id":item[13],"priority_name":item[14],"status_id":item[15],"status_name":item[16],"owner":item[17],"send_at":item[18],"created_at":item[19],"updated_at":item[20],"sent":item[21],"total":item[22]})
            time_cost = round(time.time() - start_time,2)
            total_count = resultscount[0][0][0] if resultscount[1] > 0 else 0
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,'total_count':total_count,'page':page,'length':length}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_noti_group',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def show_noti_detial():
    #查询推送详情列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    length = get_url_params('length')
    plan_id = get_url_params('plan_id')
    list_id = get_url_params('list_id')
    temple_id = get_url_params('temple_id')
    page = get_url_params('page')
    owner = get_url_params('owner')
    noti_group_id = get_url_params('noti_group_id')
    noti_id = get_url_params('id')
    mode = get_url_params('mode')
    length = int(length) if length else 50
    page = int(page) if page else 1
    if password == admin.admin_password and project and request.method == 'POST' and noti_group_id:
        #只有正确的密码才能触发动作
        add_on_where = ''
        add_on_where = add_on_where +(''' and {project}_noti.noti_group_id = {noti_group_id}'''.format(project=project,noti_group_id=int(noti_group_id)) if noti_group_id and noti_group_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti.plan_id = {plan_id}'''.format(project=project,plan_id=int(plan_id)) if plan_id and plan_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti.list_id = {list_id}'''.format(project=project,list_id=int(list_id)) if list_id and list_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti.temple_id = {temple_id}'''.format(project=project,temple_id=int(temple_id)) if temple_id and temple_id !='' else '')
        add_on_where = add_on_where +(''' and {project}_noti.id = {noti_id}'''.format(project=project,noti_id=int(noti_id)) if noti_id and noti_id !='' else '')
        if not mode or mode != 'cli' :
            add_on_where = add_on_where +(f''' and {project}_noti.owner like "%{owner}%"''' if owner and owner !='' else '')
        # print(add_on_where)
        try:
            results = show_noti_db(project=project,length=length,page=page,everywhere=add_on_where)
            resultscount = show_noti_count_db(project=project,length=length,page=page,everywhere=add_on_where)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                    temp_json.append({"noti_id":item[0],"plan_name":item[2],"list_desc":item[5],"data_id":item[8],"temple_name":item[10],"noti_group_id":item[11],"distinct_id":item[12],"type_name":item[14],"priority_name":item[17],"status_name":item[19],"owner":item[20],"recall_result":item[21],"send_at":item[22],"created_at":item[23],"updated_at":item[24]})
                else:
                    temp_json.append({"noti_id":item[0],"plan_id":item[1],"plan_name":item[2],"list_id":item[3],"list_init_date":item[4],"list_desc":item[5],"jobs_id":item[6],"list_status":item[7],"data_id":item[8],"temple_id":item[9],"temple_name":item[10],"noti_group_id":item[11],"distinct_id":item[12],"type_id":item[13],"type_name":item[14],"content":json.loads(item[15]),"priority_id":item[16],"priority_name":item[17],"status_id":item[18],"status_name":item[19],"owner":item[20],"recall_result":item[21],"send_at":item[22],"created_at":item[23],"updated_at":item[24]})
            time_cost = round(time.time() - start_time,2)
            total_count = resultscount[0][0][0] if resultscount[1] > 0 else 0
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,'total_count':total_count,'page':page,'length':length}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='show_noti_detial',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def manual_send():
    #手动推送信息
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    noti_group_id = get_url_params('noti_group_id')
    noti_id = get_url_params('noti_id')
    if password == admin.admin_password and project and request.method == 'POST':
        pending_noti = []
        pending_return = []
        status_list = [8,9,24,28] #选择推送那种类型的信息9手动24手动应用28手动推送
        try:
            if noti_group_id and not noti_id:
                for status in status_list:
                    noti_list = select_noti_group(project=project,noti_group_id=int(noti_group_id),status=status)
                    for item in noti_list[0]:
                        pending_noti.append(item)
            elif noti_id:
                for status in status_list:
                    noti_list = select_noti_single(project=project,noti_id=int(noti_id),status=status)
                    for item in noti_list[0]:
                        pending_noti.append(item)
            for noti_item in pending_noti:
                pending_return.append(send_manual(project=project,noti=noti_item))
            time_cost = round(time.time() - start_time,2)
            returnjson = {'result':'success','results_count':len(pending_noti),'timecost':time_cost,'data':pending_return}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='manual_send',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def disable_single():
    #禁用单挑推送
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    noti_id = get_url_params('noti_id')
    if password == admin.admin_password and project and request.method == 'POST' and noti_id:
        try:
            result = disable_noti_db(project=project,noti_id=noti_id)
            time_cost = round(time.time() - start_time,2)
            if result[1] > 0:
                returnjson = {'result':'success','results_count':result[1],'timecost':time_cost}
                return jsonify(returnjson)
            else:
                returnjson = {'result':'fail','results_count':result[1],'timecost':time_cost}
                return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='manual_send',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def show_scheduler_jobs():
    #查询分区任务列表
    start_time = time.time()
    password = get_url_params('password')
    project = get_url_params('project')
    length = get_url_params('length')
    page = get_url_params('page')
    mode = get_url_params('mode')
    length = int(length) if length else 50
    page = int(page) if page else 1
    if password == admin.admin_password and request.method == 'POST':
        try:
            results = show_scheduler_jobs_db(page=page,length=length)
            result_count = show_scheduler_jobs_count_db()
            time_cost = round(time.time() - start_time,2)
            temp_json = []
            for item in results[0]:
                if mode and mode =='cli':
                    temp_json.append({"scheduler_id":item[0],"project":item[1],"group_id":item[2],"list_index":item[3],"start_at":item[4],"priority_name":item[7],"status_name":item[9],"created_at":item[10],"updated_at":item[11]})
                else:
                    temp_json.append({"scheduler_id":item[0],"project":item[1],"group_id":item[2],"list_index":item[3],"start_at":item[4],"data":json.loads(item[5]),"priority_id":item[6],"priority_name":item[7],"status_id":item[8],"status_name":item[9],"created_at":item[10],"updated_at":item[11]})
            returnjson = {'result':'success','results_count':results[1],'timecost':time_cost,'data':temp_json,'total_count':result_count[0][0][0],'page':page,'length':length}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='manual_send',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def create_scheduler_jobs_manual():
    #手动创建分群任务
    project = get_url_params('project')
    plan_id = get_url_params('plan_id')
    send_at = get_url_params('send_at') if get_url_params('send_at') else int(time.time())
    password = get_url_params('password')
    if password == admin.admin_password and request.method == 'POST':
        try:
            count = 0
            plan_result,plan_count = select_usergroup_jobs_plan_manual(project=project,plan_id=plan_id)
            for plan in plan_result:
                times = get_next_time(current_time = int(send_at))
                for time_1 in times:
                    insert_result,insert_count = insert_scheduler_job(project = project,group_id = plan[0],datetime = time_1['time_int'],data = {'datetime_int':time_1['time_int'],'datetime_tuple':time_1['time_tuple'],'datetime':time.strftime("%Y-%m-%d %H:%M:%S", time_1['time_tuple']),'date':time.strftime("%Y-%m-%d", time_1['time_tuple']),'func':json.loads(plan[1])},priority=plan[3] if plan[3] else 13,status=16)
                    write_to_log(filename = 'api_noti', defname = 'create_scheduler_jobs_manual', result = '项目'+str(project)+'计划'+str(plan[0])+'已添加时间'+time.strftime("%Y-%m-%d %H:%M:%S", time_1['time_tuple']))
                    count = count+insert_count
            returnjson = {'result':'success','insert_count':count}
            return jsonify(returnjson)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='create_scheduler_jobs_manual',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)


def create_manual_temple_noti():
    #外部触发模板消息
    project = get_url_params('project')
    temple_id = get_url_params('temple_id')
    send_at = get_url_params('send_at') if get_url_params('send_at') else int(time.time())
    password = get_url_params('password')
    owner = get_url_params('owner')
    data = get_url_params('data')
    if password == admin.admin_password and request.method == 'POST' and owner and owner !='' and project:
        try:
            data_jsons = json.loads(data)
            data_list = []
            for item in data_jsons:
                print(item)
                if 'distinct_id' in item and 'data_json' in item:
                    result_temple = select_noti_temple(project=project,temple_id=temple_id)
                    result = apply_temple(project=project,temple_args=json.loads(result_temple[0][0][2]),temple_content=json.loads(result_temple[0][0][3]),data_json=item['data_json'],data_key=item['distinct_id'],send_at=send_at,group_id=None,owner=owner)
                    data_list.append(result)
            result_insert = create_non_usergroup_noti(args={'owner':owner,'temple_id':temple_id,'project':project,'data':data_list})
            return jsonify(result_insert)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='create_manual_temple_noti',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def create_manual_non_temple_noti():
    #外部触发非模板消息
    project = get_url_params('project')
    send_at = get_url_params('send_at') if get_url_params('send_at') else int(time.time())
    password = get_url_params('password')
    medium_id = get_url_params('medium_id')
    owner = get_url_params('owner')
    data = get_url_params('data')
    if password == admin.admin_password and request.method == 'POST' and owner and owner !='' and project:
        try:
            data_jsons = json.loads(data)
            data_list = []
            for item in data_jsons:
                if 'send_tracker' in item and 'distinct_id' in item['send_tracker'] and item['send_tracker']['distinct_id'] != '':
                    item['distinct_id'] = item['send_tracker']['distinct_id']
                    item['send_at'] = send_at
                    data_list.append(item)
                elif 'distinct_id' in item and item['distinct_id'] !='':
                    item['send_at'] = send_at
                    data_list.append(item)
            result = create_non_usergroup_non_temple_noti(args={'owner':owner,'project':project,'data':data_list,'medium_id':medium_id})
            return jsonify(result)
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='api_noti',defname='create_manual_temple_noti',result=error)
            returnjson = {'result':'fail','error':error}
            return jsonify(returnjson)

def show_temple_args():
    #查询模板需要的参数
    # project = get_url_params('project')
    # password = get_url_params('password')
    # data = get_url_params('data')
    # if password == admin.admin_password and request.method == 'POST' and owner and owner !='' and project:
    result_temple = select_noti_temple(project='tvcbook',temple_id=1011)
    args = json.loads(result_temple[0][0][2])
    print(args)
    for arg in args:
        for key in args[arg]:
            print(arg,key,args[arg][key])
    
if __name__ == "__main__":
    show_temple_args()