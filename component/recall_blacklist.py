# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from component.db_func import insert_update_recall_blacklist,insert_recall_blacklist_reason,select_recall_blacklist_id,insert_recall_blacklist,update_recall_blacklist,insert_recall_blacklist_history,select_recall_blacklist_list
import time


class blacklist_commit:
    def __init__(self, data):
        # self.data = data
        self.project = data['project'] if 'project' in data and data['project'] else None
        self.distinct_id = data['distinct_id'] if 'distinct_id' in data and data['distinct_id'] else None
        self.key = data['key'] if 'key' in data and data['key'] else None
        self.type = data['type'] if 'type' in data and data['type'] else None
        self.status = data['status'] if 'status' in data and data['status'] else 0
        self.reason_id = data['reason_id'] if 'reason_id' in data and data['reason_id'] else 0
        self.owner = data['owner'] if 'owner' in data and data['owner'] else None
        self.comment = data['comment'] if 'comment' in data and data['comment'] else None
        self.timenow = data['timenow'] if 'timenow' in data and data['timenow'] else int(time.time())

    def universal(self):
        select_result = select_recall_blacklist_id(key=self.key,type_id=self.type,project=self.project,limit=1)
        if select_result[0] and select_result[0][0][5] != 45:
            rbid = select_result[0][0][0]
            result = update_recall_blacklist(project=self.project,key=self.key,type_id=self.type,status=self.status,reason_id=self.reason_id,latest_owner=self.owner,distinct_id=self.distinct_id,timenow=self.timenow)
            result_reason = insert_recall_blacklist_reason(rbid=rbid,reason_id=self.reason_id,reason_owner=self.owner,final_status_id=self.status,reason_comment=self.comment,timenow=self.timenow)
            desc,status = '更新条目',1
        elif select_result[0] and select_result[0][0][5] == 45:
            desc,status = '禁止解禁状态',0
        else:
            result = insert_recall_blacklist(project=self.project,key=self.key,type_id=self.type,status=self.status,reason_id=self.reason_id,latest_owner=self.owner,distinct_id=self.distinct_id,timenow=self.timenow)
            rbid=result[2]
            result_reason = insert_recall_blacklist_reason(rbid=rbid,reason_id=self.reason_id,reason_owner=self.owner,final_status_id=self.status,reason_comment=self.comment,timenow=self.timenow)
            desc,status = '新增条目',1
        return_pending = {'result_desc':desc,'result_code':status,'input':{'key':self.key,'type':self.type,'project':self.project,'reason_id':self.reason_id,'owner':self.owner,'comment':self.comment,'distinct_id':self.distinct_id,'status':self.status}}
        return return_pending

    def pending_info(self):
        self.status = 43
        return(self.universal())
    def add_by_user(self):
        self.reason_id = 31
        return(self.universal())
    def add_by_staff_report(self):
        self.reason_id = 33
        return(self.universal())
    def add_by_wrong_address(self):
        self.reason_id = 35
        return(self.universal())
    def add_by_junk_warning(self):
        self.reason_id = 36
        return(self.universal())
    def add_by_import(self):
        self.reason_id = 37
        return(self.universal())
    def add_by_staff_idea(self):
        self.reason_id = 47
        return(self.universal())
    def remove_by_user(self):
        self.reason_id = 32
        self.status = 44
        return(self.universal())
    def remove_by_staff(self):
        self.reason_id = 34
        self.status = 44
        return(self.universal())
    def remove_by_whitelist(self):
        self.reason_id = 38
        self.status = 44
        return(self.universal())
    def remove_by_fix_mistake(self):
        self.reason_id = 46
        self.status = 44
        return(self.universal())

class blacklist_query:
    def __init__(self, data):
        # self.data = data
        self.project = data['project'] if 'project' in data and data['project'] else None
        self.distinct_id = data['distinct_id'] if 'distinct_id' in data and data['distinct_id'] else None
        self.key = data['key'] if 'key' in data and data['key'] else None
        self.type = data['type'] if 'type' in data and data['type'] else None
        self.status = data['status'] if 'status' in data and data['status'] else None
        self.limit = data['limit'] if 'limit' in data and data['limit'] else None
        self.owner = data['owner'] if 'owner' in data and data['owner'] else None
        self.start = data['start'] if 'start' in data and data['start'] else None
        self.level = int(data['level']) if 'level' in data and data['level'] and data['level'] != '' and data['level'] !=' ' else None

    def universal_list(self):
        result = select_recall_blacklist_list(type_id=self.type,distinct_id=self.distinct_id,project=self.project,status=self.status,start=self.start,limit=self.limit)
        return_pending={'data':[],'input':{'type':self.type,'project':self.project,'distinct_id':self.distinct_id,'status':self.status}}
        return_pending['count'] = result[1]
        for item in result[0]:
            return_pending['data'].append({'id':item[0],'reason_id':item[1],'reason_name':item[2],'owner':item[3],'latest_owner':item[4],'status':item[5],'status_name':item[6],'created_at':item[7],'updated_at':item[8]})
        return return_pending

    def universal_status(self):
        return_pending = {'result_desc':'未找到黑名单信息','result_code':44,'input':{'key':self.key,'type':self.type,'project':self.project,'owner':self.owner,'distinct_id':self.distinct_id,'status':self.status}}
        select_result = select_recall_blacklist_id(key=self.key,distinct_id=self.distinct_id,type_id=self.type,project=self.project,status=self.status,limit=self.limit)
        if select_result[0]:
            reason_history = []
            # print(select_result[0])
            for item in select_result[0]:
                reason_history.append({"reason_id":item[11],"reason_name":item[12],"owner":item[13],"reason_comment":item[14],'reason_time':item[15],'status_id':item[9],'status_name':item[10]})
            return_pending = {'result_desc':select_result[0][0][6],'result_code':select_result[0][0][5],'final_reason_id':select_result[0][0][1],'final_reason_name':select_result[0][0][2],'init_owner':select_result[0][0][3],'final_owner':select_result[0][0][4],'init_time':select_result[0][0][7],'update_time':select_result[0][0][8],'input':{'key':self.key,'type':self.type,'project':self.project,'owner':self.owner,'distinct_id':self.distinct_id,'status':self.status},"reason_history":reason_history,"reason_count":select_result[1]}
            insert_recall_blacklist_history(rbid=select_result[0][0][0],checker=self.owner,result_status_id=select_result[0][0][5],result_reason_id=select_result[0][0][1])
        return return_pending

    def check_ad(self):
        self.status = [40,41,45]
        return self.universal_status()

    def check_noti(self):
        self.status = [40,42,45]
        return self.universal_status()

    def check_event(self):
        self.status = [40,41,45,54]
        return self.universal_status()

    def check_ad_list(self):
        self.status = [40,41,45]
        return self.universal_list()

    def check_noti_list(self):
        self.status = [40,42,45]
        return self.universal_list()

    def check_event_list(self):
        self.status = [40,41,45,54]
        return self.universal_list()

    def check_messenger(self):
        if self.level == 49:
            self.status = [0]
            return self.universal_status()
        elif self.level == 50 or self.level == 51:
            return self.check_noti()
        elif self.level == 52:
            return self.check_event()
        elif self.level == 53:
            return self.check_ad()
        else:
            return self.check_ad()