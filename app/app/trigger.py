# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from app.trigger_jobs.sample import *
import traceback
from app.configs.export import write_to_log
from app.component.kafka_op import get_message_from_kafka_independent_listener


class trigger:
    def __init__(self, project, data_decode):
        self.data = data_decode
        self.project = project
        self.distinct_id = data_decode['distinct_id']

    def sample(self):
        if self.data and 'event' in self.data and self.data['event'] == 'RegisterLogin' and 'properties' in self.data and 'action' in self.data['properties'] and self.data['properties']['action'] == 147 and 'login_type' in self.data['properties'] and self.data['properties']['login_type'] == 1:
            recall_baidu_bdvid(uid=self.distinct_id, project=self.project, newType=49, convertValue=0)
        elif self.data and 'event' in self.data and self.data['event'] == 'vipPurchase' and 'properties' in self.data and 'action' in self.data['properties'] and self.data['properties']['action'] == 34:
            recall_baidu_bdvid(uid=self.distinct_id, project=self.project, newType=10, convertValue=self.data['properties']['totalpay_sum_fix'] if 'totalpay_sum_fix' in self.data['properties'] else 0)

    def play_all(self):
        try:
            self.sample()
            if self.project and self.project == 'sample':
                self.sample()
        except Exception:
            error = traceback.format_exc()
            write_to_log(filename='trigger',defname='play_all',result=error)


if __name__ == "__main__":
    results = get_message_from_kafka_independent_listener()
    for item in results :
        group = json.loads(item.value.decode('utf-8'))['group'] if "group" in json.loads(item.value.decode('utf-8')) else None
        data = json.loads(item.value.decode('utf-8'))['data']
        offset = item.offset
        if group == 'event_track':
            a = trigger(project=data['project'], data_decode=data['data_decode'])
            a.play_all()