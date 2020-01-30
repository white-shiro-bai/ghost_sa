# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from kafka import KafkaProducer, KafkaConsumer
import json
from configs import kafka
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)



producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
def insert_message_to_kafka(msg):
    producer.send(topic=kafka.kafka_topic,value=json.dumps(msg).encode())

def get_message_from_kafka():
    consumer=KafkaConsumer(
        kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id)
    return consumer

if __name__ == "__main__":
    insert_message_to_kafka(msg={'msg': 'test'})
    # get_message_from_kafka()
