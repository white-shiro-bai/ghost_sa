# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
import json
from configs.export import write_to_log
from component.e_mail import send_email
from component.db_func import insert_event,update_noti,select_noti_auto,select_scheduler_enable_project,update_noti_group
import traceback
import time


class send:
    def __init__(self, data):
        self.data = data
        self.noti_id = data[0]
        self.noti_group_id = data[1]
        self.noti_type = data[2]
        self.noti_content = json.loads(data[3])

    def sample(self):
        if self.data:
            pass

    def via_email(self):
        default_mail_from = self.noti_content['mail_from'] if 'mail_from' in self.noti_content and self.noti_content['mail_from'] and self.noti_content['mail_from'] != '' else 'accounts-noreply@notify.tvcbook.com'#默认发送邮箱
        result = send_email(to_addr=self.noti_content['mail_to'],from_addr=default_mail_from,subject=self.noti_content['subject'],html=self.noti_content['content'])
        return result
    def sms(self):
        pass
        return 2
    def wechat_official_account(self):
        pass
    def wechat_subscriptions(self):
        pass
    def wechat_miniprogram(self):
        pass
    def umeng_u_push(self):
        pass
    def pm(self):
        pass

    def play_all(self):
        try:
            print(self.noti_type)
            if self.noti_type == 23:
                return self.via_email()
            elif self.noti_type == 24:
                return self.sms()
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='messenger',defname='play_all',result=error)
            return 'failed,please check logs'


def send_manual(project,noti):
    import platform
    # print(noti)
    v = send(data=noti)
    send_result = v.play_all()
    timenow=int(time.time())
    if send_result :
        if send_result == 'success':
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

if __name__ == "__main__":
    send_auto_noti()