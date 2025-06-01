# -*- coding: utf-8 -*-
#
#Date: 2022-03-12 14:54:46
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2025-06-01 15:53:56
#FilePath: \ghost_sa_github_cgq\component\kafka_op.py
#
import sys
sys.path.append('./')
from kafka import KafkaProducer, KafkaConsumer
import json
from configs import kafka
from configs import admin


if admin.use_kafka is True:
    producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)

def insert_message_to_kafka(key, msg):
    if isinstance(key, str):
        key = key.encode()
    else:
        key = None
    producer.send(topic=kafka.kafka_topic, key=key, value=json.dumps(msg).encode())


kafka_offset_reset = 'earliest' #latest,earliest,none 首次拉取kafka订阅的模式

def get_message_from_kafka(group_id=kafka.client_group_id,client_id=kafka.client_id):
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=group_id,auto_offset_reset=kafka.kafka_offset_reset,client_id=client_id,metadata_max_age_ms= 1 * 60 * 1000)
    return consumer

if __name__ == "__main__":
    # producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
    # insert_message_to_kafka(key='123231231', msg={'msg': 'test'})
    res = get_message_from_kafka()
    for item in res :
        print(item.value.decode('utf-8'))
