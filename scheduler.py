# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.public_value import get_next_time,get_priority
from component.db_func import select_scheduler_enable_project,select_usergroup_jobs_plan,insert_scheduler_job,check_next_scheduler_job,update_scheduler_job,select_noti_temple,select_usergroup_data,insert_noti,insert_noti_group,update_noti_group,select_usergroupdata_data,update_usergroup_plan,update_usergroup_list,select_auto_temple_apply_plan,update_noti_temple
from configs.export import write_to_log
import json
import time
import importlib
import traceback
from scheduler_jobs.etl_model import apply_temple




def get_task_day():
    projects_result,project_count = select_scheduler_enable_project()
    write_to_log(filename='scheduler', defname='get_task_day', result='获取启用定时器任务的项目'+ (str(project_count) if project_count else '0'))
    for project in projects_result:
        plan_result,plan_count = select_usergroup_jobs_plan(project=project[0])
        write_to_log(filename='scheduler', defname='get_task_day', result='查询到项目'+project[0]+'含有可用计划'+ (str(plan_count) if plan_count else '0'))
        for plan in plan_result:
            times = get_next_time(timer = plan[2],current_time = int(time.time()))
            for time_1 in times:
                func_loads = json.loads(plan[1])
                func_loads['args']['noti_status'] = plan[4]
                insert_scheduler_job(project = project[0],group_id = plan[0],datetime = time_1['time_int'],data = {'datetime_int':time_1['time_int'],'datetime_tuple':time_1['time_tuple'],'datetime':time.strftime("%Y-%m-%d %H:%M:%S", time_1['time_tuple']),'date':time.strftime("%Y-%m-%d", time_1['time_tuple']),'func':func_loads},priority=plan[3] if plan[3] else 13,status=16)
                write_to_log(filename = 'scheduler', defname = 'get_task_day', result = '项目'+str(project[0])+'计划'+str(plan[0])+'已添加时间'+time.strftime("%Y-%m-%d %H:%M:%S", time_1['time_tuple']))
            write_to_log(filename = 'scheduler', defname = 'get_task_day', result = '项目'+str(project[0])+'计划'+str(plan[0])+'已添加计划条目'+str(len(times)))
def do_all_task():
    task_count = 0
    start_time = int(time.time())
    miss = 1
    while task_count < 1 and int(time.time())-start_time <=1800:
        #连续30分钟拿不到任务，就退出，会重新搜索plan。
        priority = get_priority()
        task_result,task_count = check_next_scheduler_job(priority=priority)
        write_to_log(filename='scheduler', defname='do_all_task', result='查询优先级'+str(priority)+'获取任务数'+str(task_count))
        if task_count == 0 and priority == 13 :
            #如果遇到低优先级无任务，则休息5分钟以减少数据库请求的次数。此处没做低优先级没命中继续上查高优先级如果也没有再休息的功能。如果写了，效率可以更高，按照高优先级，中优先级，低优先级1:1:1的比例排任务，最高每1000次任务执行能减少10分钟的等待时间。
            miss = miss * 2
            #延迟器，用来降低数据库压力，每次找不到，则增加1秒的重试等待时间。当重试等待超过5分钟后，不再增加重试等待时间。以保证5分钟至少会查询一次。
            if miss >=0 and miss <= 300:
                time.sleep(abs(miss))
            elif miss > 300:
                time.sleep(300)
            print('miss记数器',miss)
        elif task_count >=1:
            miss = 1
            data = json.loads(task_result[0][4])
            data['group_id'] = task_result[0][2]
            update_scheduler_job(jobid=task_result[0][0],status=17)
            py = importlib.import_module(data['func']['dir'])
            ff = getattr(py, data['func']['name'])
            # print(data['func']['args'])
            update_scheduler_job(jobid=task_result[0][0],status=18)
            for arg in data['func']['args']:
                if type(data['func']['args'][arg]) is str and '___' in data['func']['args'][arg]:
                    data['func']['args'][arg] = data[data['func']['args'][arg].replace('___','')]
            # print(data['func']['args'])
            data['func']['args']['job_id']=task_result[0][0]
            data['func']['args']['group_id'] = task_result[0][2]
            try:
                write_to_log(filename='scheduler', defname='do_all_task', result='优先级'+str(priority)+'任务id'+str(task_result[0][0])+'拼接的任务参数'+str(data)+'开始执行')
                func_result,list_index = ff(data['func']['args'])
                update_scheduler_job(jobid=task_result[0][0],list_index=list_index,status=19)
                write_to_log(filename='scheduler', defname='do_all_task', result='优先级'+str(priority)+'任务id'+str(task_result[0][0])+'拼接的任务参数'+str(data)+'执行完毕')
            except Exception:
                error = traceback.format_exc()
                write_to_log(filename='scheduler', defname='do_all_task', result=error)
                update_scheduler_job(jobid=task_result[0][0],status=21)
            task_count = task_count - 1


def create_noti_group(project,temple_id,user_group_id=None,data_id=None,owner='noti',send_at=None):
    #对分群应用模板，有data_id时，优先使用data_id
    result_temple = select_noti_temple(project=project,temple_id=temple_id)
    if not user_group_id and not data_id:
        return 'no_group'
    else:
        if user_group_id and not data_id:
            result_data = select_usergroup_data(project=project,group_list_id=user_group_id)
        elif data_id:
            result_data = select_usergroupdata_data(project=project,data_id=data_id)
        timenow = int(time.time())
        result_group = insert_noti_group(project=project,plan_id=result_data[0][0][0],list_id=result_data[0][0][1],data_id=result_data[0][0][2],temple_id=result_temple[0][0][0],owner=owner,send_at=send_at if send_at else timenow,sent=0,total=result_data[1],priority=13,status=result_data[0][0][6])
        for noti in result_data[0]:
            timenow = int(time.time())
            temple_content = apply_temple(project=project,temple_args=json.loads(result_temple[0][0][2]),temple_content=json.loads(result_temple[0][0][3]),data_json=json.loads(noti[5]),data_key=noti[4],group_id=user_group_id,owner=owner,send_at=send_at if send_at else timenow)
            insert_result = insert_noti(project=project,type_1=json.loads(result_temple[0][0][2])['meta']['medium_id'],created_at=timenow,updated_at=timenow,distinct_id=noti[4],content=temple_content,send_at=send_at if send_at else timenow,plan_id=noti[0],list_id=noti[1],data_id=noti[2],temple_id=result_temple[0][0][0],noti_group_id=result_group[2],priority=13,status=noti[6],owner=owner,recall_result=None,key=temple_content['key'] if 'key' in temple_content else None,level=temple_content['level'] if 'level' in temple_content else None)
        update_noti_temple(project=project,temple_id=temple_id,apply_times=1,lastest_apply_time=timenow,lastest_apply_list=user_group_id if user_group_id else 0)
        update_noti_group(project=project,noti_group_id=result_group[2])
        update_usergroup_list(project=project,list_id=result_data[0][0][1],apply_temple_times=1)
        update_usergroup_plan(project=project,plan_id=result_data[0][0][0],latest_apply_temple_id=temple_id,latest_apply_temple_time=timenow)
        return 'success'


def create_auto_group():
    projects_result,project_count = select_scheduler_enable_project()
    write_to_log(filename='scheduler', defname='create_auto_group', result='获取项目列表'+ (str(project_count) if project_count else '0'))
    for project in projects_result:
        result_auto_noti = select_auto_temple_apply_plan(project=project[0])
        # print(result_auto_noti)
        for data_list in result_auto_noti[0]:
            # print(data_list)
            func_data = json.loads(data_list[2])
            # print(func_data)
            id_list = []
            if "default_temple" in func_data and type(func_data["default_temple"]) is list:
                for temple_id in func_data["default_temple"]:
                    id_list.append(temple_id)
            elif "default_temple" in func_data and type(func_data["default_temple"]) is int:
                id_list.append(func_data["default_temple"])
            for tid in id_list:
                send_at = []
                result_temple = select_noti_temple(project=project[0],temple_id=tid)
                if result_temple[1]>0 and result_temple[0][0][2]:
                    args = json.loads(result_temple[0][0][2])
                    if 'meta' in args and 'default_send_time' in args['meta']:
                        print(args['meta']['default_send_time'])
                        send_at_list = get_next_time(timer = args['meta']['default_send_time'],current_time = int(time.time()))
                        # org_data_time_list = get_next_time(timer = args['meta']['default_send_time'],current_time=data_list[3])
                        # if send_at_list == send_at_list :
                        for time_return in send_at_list:
                            send_at.append(time_return['time_int'])
                    elif len(send_at)==0:
                        send_at.append(int(time.time()))
                    for send_int in send_at:
                        create_noti_group(project=project[0],temple_id=tid,user_group_id=data_list[1],data_id=None,owner='create_auto_group',send_at=send_int)


def keep_alive():
    while True:
        get_task_day()
        do_all_task()
        create_auto_group()

if __name__ == "__main__":
    keep_alive()