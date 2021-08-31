# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
# from os import add_dll_directory
import sys
# from threading import Event
# from traceback import print_exception
sys.path.append("./")
sys.setrecursionlimit(10000000)
from app.configs import admin, kafka
import time 
from app.component.public_func import show_my_memory
from app.component.db_func import show_project,select_properties,insert_update_access_control_list
import json
import traceback
from app.configs.export import write_to_log

class access_control:

    def __init__(self,project=None):
        # self.ip_group = {}
        # self.ip = {}
        # self.distinct_id = {}
        self.projects = project if project else {}
        # self.customized = {}
        self.start_time = int(time.time())
        self.check_mem_start = int(time.time())
        self.my_memory = 0
        self.term_times = {'distinct_id':1,'add_on_key':1,'ip':admin.access_control_distinct_id_per_ip,'ip_group':admin.access_control_distinct_id_per_ip*admin.access_control_ip_per_ip_group}

    def check_mem(self):
        #每30秒检查一次内存占用量
        if int(time.time()-self.check_mem_start) <= 30 and self.projects != {}:
            return self.my_memory
        else:
            self.my_memory = int(show_my_memory())
            self.check_mem_start = int(time.time())
            return self.my_memory

    def refresh_threshold_list(self):
        self.threshold_list = {}
        project_list = show_project()[0]
        for project in project_list:
            if project[0] not in self.threshold_list:
                self.threshold_list[project[0]] = {}
            if project[4]:
                self.threshold_list[project[0]]['default_sum'] = project[4]
            if project[5]:
                self.threshold_list[project[0]]['default_event'] = project[5]
            event_threshold_list = select_properties(project=project[0])[0]
            for item in event_threshold_list:
                if item[0] not in self.threshold_list[project[0]]:
                    self.threshold_list[project[0]][item[0]] = item[1]
        # print(self.threshold_list)

    def insert_data(self,project,key,type_str,event,pv,hour,date):
        type_int={'ip':60,'ip_group':61,'distinct_id':62,'add_on_key':63}
        insert_update_access_control_list(project=project,key=key,type_int=type_int[type_str],event=event,pv=pv,date=date,hour=hour)


    def etl(self):
        self.refresh_threshold_list()
        date = time.strftime("%Y-%m-%d", time.localtime())
        hour = int(time.strftime("%H", time.localtime()))
        for projects_project in self.projects:
            if projects_project in self.threshold_list:
                for projects_project_event in self.projects[projects_project]:
                    if self.projects[projects_project][projects_project_event] == 'all' :
                        #如果event是all的触发量。如果没有则使用全局总量
                        if 'all' in self.threshold_list[projects_project]:
                            limit = self.threshold_list[projects_project]['all']
                        elif 'default_sum' in self.threshold_list[projects_project]:
                            limit = self.threshold_list[projects_project]['all']['default_sum']
                        else:
                            limit =  admin.access_control_sum_count
                    elif self.projects[projects_project][projects_project_event] != '' :
                        #event不是all的触发量。如果没有，则使用项目阈值，如果再没有，则使用全局事件量
                        if projects_project_event in self.threshold_list[projects_project]:
                            limit = self.threshold_list[projects_project][projects_project_event]
                        elif 'default_event' in self.threshold_list[projects_project]:
                            limit = self.threshold_list[projects_project]['default_event']
                        else:
                            limit = admin.access_control_event_default
                    for term in self.projects[projects_project][projects_project_event]:
                        #比对项目与限制值
                        for content in self.projects[projects_project][projects_project_event][term]:
                            if self.projects[projects_project][projects_project_event][term][content] >= limit*self.term_times[term]*admin.access_control_max_window/3600:
                                self.insert_data(project=projects_project,key=content,type_str=term,event=projects_project_event,pv=self.projects[projects_project][projects_project_event][term][content],hour=hour,date=date)
            elif projects_project:
                for projects_project_event in self.projects[projects_project]:
                    if self.projects[projects_project][projects_project_event] == 'all' :
                        limit =  admin.access_control_sum_count
                    else:
                        limit = admin.access_control_event_default
                    for term in self.projects[projects_project][projects_project_event]:
                        #比对项目与限制值
                        for content in self.projects[projects_project][projects_project_event][term]:
                            if self.projects[projects_project][projects_project_event][term][content] >= limit*self.term_times[term]*admin.access_control_max_window/3600:
                                self.insert_data(project=projects_project,key=content,type_str=term,event=projects_project_event,pv=self.projects[projects_project][projects_project_event][term][content],hour=hour,date=date)
        self.projects = {}
        self.start_time = int(time.time())
        self.my_memory = int(show_my_memory())

    def update_data(self,project,event,term,content):
        if term not in self.projects[project]['all']:
            self.projects[project]['all'][term] = {}
        self.projects[project]['all'][term][content] = self.projects[project]['all'][term][content] + 1 if content in self.projects[project]['all'][term] else 1
        if event:
            if term not in self.projects[project][event]:
                self.projects[project][event][term] = {}
            self.projects[project][event][term][content] = self.projects[project][event][term][content] + 1 if content in self.projects[project][event][term] else 1

    def commit(self,project=None,event=None,ip_commit=None,distinct_id_commit=None,add_on_key_commit=None):
        if ip_commit:
            ip_group_commit = '.'.join(ip_commit.split('.')[0:3])
            self.update_data(project=project,event=event,term='ip',content=ip_commit)
            self.update_data(project=project,event=event,term='ip_group',content=ip_group_commit)
        if distinct_id_commit:
            self.update_data(project=project,event=event,term='distinct_id',content=distinct_id_commit)
        if add_on_key_commit:
            self.update_data(project=project,event=event,term='add_on_key',content=add_on_key_commit)
    
    def traffic(self,project=None,event=None,ip_commit=None,distinct_id_commit=None,add_on_key_commit=None):
        if project and project not in self.projects:
            self.projects[project] = {}
        if 'all' not in self.projects[project]:
            self.projects[project]['all'] = {'ip_group':{},'ip':{},'distinct_id':{},'add_on_key':{}}
        if event not in self.projects[project]:
            self.projects[project][event] = {'ip_group':{},'ip':{},'distinct_id':{},'add_on_key':{}}
        if int(time.time())-self.start_time >= admin.access_control_max_window or self.check_mem() >= admin.access_control_max_memory:
            write_to_log(filename='access_control', defname='traffic', result='开始清理:'+str(self.check_mem()))
            self.etl()
            write_to_log(filename='access_control', defname='traffic', result='完成清理:'+str(self.check_mem()))
            self.traffic(project=project,event=event,ip_commit=ip_commit,distinct_id_commit=distinct_id_commit,add_on_key_commit=add_on_key_commit)
        else:
            self.commit(project=project,event=event,ip_commit=ip_commit,distinct_id_commit=distinct_id_commit,add_on_key_commit=add_on_key_commit)
            # print('commit')


if __name__ == "__main__":
    if admin.access_control_commit_mode =='access_control':
        from app.component.access_control import access_control
        from app.utils.kafka_op import get_message_from_kafka
        ac_access_control = access_control()
        results = get_message_from_kafka(group_id=kafka.client_group_id+'_'+admin.access_control_kafka_client_group_id,client_id=kafka.client_id+'_'+admin.access_control_kafka_client_client_id)
        for item in results :
            group = json.loads(item.value.decode('utf-8'))['group'] if "group" in json.loads(item.value.decode('utf-8')) else None
            data = json.loads(item.value.decode('utf-8'))['data']
            offset = item.offset
            if group == 'event_track':
                try:
                    ac_access_control.traffic(project=data['project'],event=data['data_decode']['event'] if 'event' in data['data_decode'] else None,ip_commit=data['ip'],distinct_id_commit=data['data_decode']['distinct_id'],add_on_key_commit=data['data_decode']['properties'][admin.access_control_add_on_key] if admin.access_control_add_on_key in data['data_decode']['properties'] else None)
                except Exception:
                    error = traceback.format_exc()
                    write_to_log(filename='access_control', defname='main', result=error)