# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import json
from configs.export import write_to_log
from component.e_mail import send_email
from component.we_chat import post_wechat_notification
from component.db_func import insert_event, insert_recall_blacklist_reason,update_noti,select_noti_auto,select_scheduler_enable_project,update_noti_group,insert_noti_group,insert_noti,select_noti_temple,update_noti_temple
# from scheduler_jobs.etl_model import apply_temple
import traceback
import time
from configs import admin
from component.recall_blacklist import blacklist_commit,blacklist_query
from component.umail import send_umail
from configs import email,umail


class send:
    def __init__(self, data,project):
        self.data = data
        self.project = project
        self.noti_id = data[0]
        self.noti_group_id = data[1]
        self.noti_type = data[2]
        self.noti_content = json.loads(data[3])
        self.distinct_id = data[4]


    def sample(self):
        if self.data:
            pass

    def via_email(self):
        default_mail_from = self.noti_content['mail_from'] if 'mail_from' in self.noti_content and self.noti_content['mail_from'] and self.noti_content['mail_from'] != '' else email.mail_user #默认发送邮箱
        result = send_email(to_addr=self.noti_content['mail_to'],from_addr=default_mail_from,subject=self.noti_content['subject'],html=self.noti_content['content'])
        return result

    def via_umail(self):
        default_mail_from = self.noti_content['mail_from'] if 'mail_from' in self.noti_content and self.noti_content['mail_from'] and self.noti_content['mail_from'] != '' else umail.umail_user#默认发送邮箱
        result = send_umail(to_addr=self.noti_content['mail_to'],from_addr=default_mail_from,subject=self.noti_content['subject'],html=self.noti_content['content'])
        return result

    def sms(self):
        pass
        return 2
    def wechat_official_account(self):
        # content = json.loads(self.noti_content)
        # print(content['data'])
        # content['data'] = json.loads(content['data'])
        # print(content)
        result = post_wechat_notification(data=json.loads(self.noti_content['content']))
        return result
    def wechat_subscriptions(self):
        pass
    def wechat_miniprogram(self):
        pass
    def umeng_u_push(self):
        pass
    def pm(self):
        pass

    def sent_all(self):
        try:
            print(self.noti_type)
            if self.noti_type == 23:
                return self.via_email()
            elif self.noti_type == 24:
                return self.sms()
            elif self.noti_type == 29:
                return self.wechat_official_account()
            elif self.noti_type == 81:
                return self.via_umail()
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='messenger',defname='play_all',result=error)
            return 'failed,please check logs'
    
    def commit_all(self):
        if admin.recall_blacklist_commit is False:
            return self.sent_all()
        elif admin.recall_blacklist_commit is True:
            result = self.sent_all()
            if result == 'success':
                return result
            elif result !='success':
                commit = blacklist_commit(data={'project':self.project,'type':self.noti_type,'key':self.noti_content['key'],'reason_id':35,'status':40,'owner':'messenger.py','comment':result,'distinct_id':self.distinct_id})
                commit.add_by_wrong_address()
                return result

    def play_all(self):
        if admin.recall_blacklist_query is True and 'key' in self.noti_content:
            checker = blacklist_query(data={'project':self.project,'type':self.noti_type,'owner':'messenger.py','key':self.noti_content['key'],'level':self.noti_content['level'] if 'level' in self.noti_content else None,'limit':1})
            blacklist_status =  checker.check_messenger()
            if blacklist_status['result_code'] == 44:
                return self.commit_all()
            else:
                return blacklist_status['result_desc']
        elif admin.recall_blacklist_query is True and 'key' not in self.noti_content:
            return '开启了黑名单校验但content未包含key'
        else:
            return self.commit_all()

def send_manual(project,noti):
    import platform
    # print(noti)
    v = send(data=noti,project=project)
    send_result = v.play_all()
    timenow=int(time.time())
    if send_result :
        if 'success' in send_result or 'ok' in send_result:
            update_noti(project=project,noti_id=noti[0],updated_at=timenow,status=26,recall_result=send_result)
            update_noti_group(project=project,noti_group_id=noti[1],sent=1)
        else:
            update_noti(project=project,noti_id=noti[0],updated_at=timenow,status=27,recall_result=send_result)
        content = json.loads(noti[3])
        if "send_tracker" in content:
            send_tracker = content["send_tracker"]
        else :
            send_tracker = {"properties":{}}
        remark = None
        if "ghost_sa" in content and "remark" in content["ghost_sa"]:
            remark = content["ghost_sa"]["remark"]
        send_tracker['properties']['sent_result'] = send_result
        # print(send_tracker)
        insert_event(table=project,alljson=json.dumps(send_tracker),track_id=0,distinct_id=noti[4],lib='noti',event='recall',type_1='track',User_Agent='',Host='',Connection='',Pragma='',Cache_Control='',Accept='',Accept_Encoding='',Accept_Language='',ip='',ip_city='{}',ip_asn='{}',url='',referrer='',remark=remark,ua_platform=platform.system(),ua_browser='',ua_version='',ua_language='')
        return noti[0],send_result
    return 'no_result'


def send_auto_noti():
    miss = 1 #初始化没有命中的次数
    while True:
        missTime = 0
        #延迟器，用来降低数据库压力，每次找不到，则增加1秒的重试等待时间。当重试等待超过2分钟后，不再增加重试等待时间。以保证2分钟至少会查询一次。
        projects_result,project_count = select_scheduler_enable_project()
        write_to_log(filename='messenger', defname='send_auto_noti', result='获取启用定时器任务的项目'+ (str(project_count) if project_count else '0'))
        for project in projects_result:
            result = select_noti_auto(project=project[0])
            if result[1] > 0 :
                miss = 1
                for noti in result[0]:
                    send_manual(project=project[0],noti=noti)
            else:
                miss = miss * 2
                missTime = missTime + 1
                print(project[0]+'暂无自动消息,miss:'+str(miss))
        if missTime == project_count and miss >=0 and miss <= 120:
            time.sleep(abs(miss))
        elif missTime == project_count and miss > 120:
            time.sleep(120)
        elif missTime < project_count:
            miss = 1

def create_non_usergroup_noti(args):
    #手动创建不在用户分群里的消息
    start_time = int(time.time())
    if 'data' in args and args['data'] and args['data'] !='' and 'project' in args and args['project'] !='':
        owner = args['owner'] if 'owner' in args else 'undefined'
        status = int(args['status']) if 'status' in args and args['status'] is not None else 9
        if 'temple_id' in args and args['temple_id'] != '':
            result_temple = select_noti_temple(project=args['project'],temple_id=args['temple_id'])
        if 'result_temple' in dir():
            medium_id = json.loads(result_temple[0][0][2])['meta']['medium_id']
        elif 'medium_id' in args:
            medium_id = args['medium_id']
        send_at = args['send_at'] if 'send_at' in args else int(time.time())
        result_group = insert_noti_group(project=args['project'],plan_id=None,list_id=None,data_id=None,temple_id=args['temple_id'] if 'temple_id' in args else None,owner=owner,send_at=send_at,sent=0,total=len(args['data']),priority=13,status=status)
        inserted = 0
        for noti in args['data']:
            if 'send_tracker' in noti and 'distinct_id' in noti['send_tracker'] and noti['send_tracker']['distinct_id'] != '':
                insert_result = insert_noti(project=args['project'],type_1=medium_id,created_at=int(time.time()),updated_at=int(time.time()),distinct_id=noti['send_tracker']['distinct_id'],content=noti,send_at=noti['send_at'] if 'send_at' in noti else send_at,plan_id=None,list_id=None,data_id=None,temple_id=result_temple[0][0][0],noti_group_id=result_group[2],priority=13,status=status,owner=owner,recall_result=None,key=noti['key'] if 'key' in noti else None,level=noti['level'] if 'level' in noti else None)
                inserted = inserted+insert_result[1]
        if 'temple_id' in args and args['temple_id'] != '':
            update_noti_temple(project=args['project'],temple_id=args['temple_id'],apply_times=1,lastest_apply_time=int(time.time()),lastest_apply_list = 0)
        update_noti_group(project=args['project'],noti_group_id=result_group[2])
        return {'result':'success','inserted':inserted,'timecost':int(time.time())-start_time}
    else:
        return {'result':'failed','error':'no_distinct_id_or_miss_data'}

def create_non_usergroup_non_temple_noti(args):
    #手动创建不在用户分群，也不适用模板的消息
    start_time = int(time.time())
    if 'data' in args and args['data'] and args['data'] !='' and 'project' in args and args['project'] !='' and 'medium_id' in args:
        owner = args['owner'] if 'owner' in args else 'undefined'
        status = int(args['status']) if 'status' in args and args['status'] is not None else 9
        send_at = args['send_at'] if 'send_at' in args else int(time.time())
        result_group = insert_noti_group(project=args['project'],plan_id=None,list_id=None,data_id=None,temple_id=None,owner=owner,send_at=send_at,sent=0,total=len(args['data']),priority=13,status=status)
        inserted = 0
        for item in args['data']:
            insert_result = insert_noti(project=args['project'],type_1=args['medium_id'],created_at=int(time.time()),updated_at=int(time.time()),distinct_id=item['distinct_id'],content=item,send_at=item['send_at'] if 'send_at' in item else send_at,plan_id=None,list_id=None,data_id=None,temple_id=None,noti_group_id=result_group[2],priority=13,status=status,owner=owner,recall_result=None,key=item['key'] if 'key' in item else None,level=item['level'] if 'level' in item else None)
            inserted = inserted+insert_result[1]
        update_noti_group(project=args['project'],noti_group_id=result_group[2])
        return {'result':'success','inserted':inserted,'timecost':int(time.time())-start_time}
    else:
        return {'result':'failed','error':'no_distinct_id_or_miss_data'}

if __name__ == "__main__":
    send_auto_noti()