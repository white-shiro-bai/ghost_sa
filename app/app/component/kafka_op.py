# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys

from flask import g, current_app

sys.path.append("./")
sys.setrecursionlimit(10000000)
from kafka import KafkaProducer, KafkaConsumer
import json
from app.configs import kafka
from app.configs import admin


def get_kafka_producer():
    if 'kafka_producer' not in g:
        g.kafka_producer = KafkaProducer(bootstrap_servers=current_app.config['BOOTSTRAP_SERVERS'])

    return g.kafka_producer


def insert_message_to_kafka(key, msg):
    if isinstance(key, str):
        key = key.encode()
    else:
        key = None
    get_kafka_producer().send(topic=kafka.kafka_topic, key=key, value=json.dumps(msg).encode())


kafka_offset_reset = 'earliest' #latest,earliest,none 首次拉取kafka订阅的模式


def get_message_from_kafka():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka')
    return consumer


def get_message_from_kafka_independent_listener():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=admin.independent_listener_kafka_client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka_independent_listener')
    return consumer


if __name__ == "__main__":
    insert_message_to_kafka(key='123231231', msg={'msg': 'test'})