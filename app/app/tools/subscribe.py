# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
from kafka import KafkaConsumer
from geoip.geo import get_asn,get_addr
from app.component.api import insert_data
from app.configs import admin
import json
import pprint

#这个工具用来在迁移过程中，实时订阅神策官方服务端的数据。使得在迁移过程中，神策官方版和鬼策

def realtime_subscribe(broker):
    consumer = KafkaConsumer('event_topic',bootstrap_servers=[broker])
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        # pprint.pprint(message.value.decode('utf-8'))
        json_data = json.dumps(data)
        # pprint.pprint(json_data)
        remark = ''
        project = data['project']
        ua_platform = data['properties']['$os'] if '$os' in data['properties'] else '' #客户端操作系统
        ua_browser = data['properties']['$browser'] if '$browser' in data['properties'] else '' #客户端的浏览器
        ua_version = data['properties']['$browser_version'] if '$browser_version' in data['properties'] else '' #客户端浏览器的版本
        ip = data['properties']['$ip'] if '$ip'in data['properties'] else ''
        ip_city,ip_is_good = get_addr(ip)
        ip_asn,ip_asn_is_good = get_asn(ip)
        if ip_is_good ==0:
            ip_city = '{}'
        if ip_asn_is_good ==0:
            ip_asn = '{}'
        referrer = data['properties']['$latest_referrer'] if '$latest_referrer' in data['properties'] else ''
        insert_data(project=project,data_decode=data,User_Agent='',Host='',Connection='',Pragma='',Cache_Control='',Accept='',Accept_Encoding='',Accept_Language='',ip=ip,ip_city=ip_city,ip_asn=ip_asn,url='',referrer=referrer,remark=remark,ua_platform=ua_platform,ua_browser=ua_browser,ua_version=ua_version,ua_language='',ip_is_good=ip_is_good,ip_asn_is_good=ip_asn_is_good,use_kafka=admin.use_kafka)


# consumer = KafkaConsumer('event_topic',bootstrap_servers=['data.tvcbook.sa:9092'])
# for message in consumer:
#         # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
#         print(message.value.decode('utf-8'))

if __name__ == "__main__":
    realtime_subscribe(broker='your_sa_kafka:9092')#从神策kafka上订阅数据到鬼策。二者同时进数据，都是完整的。