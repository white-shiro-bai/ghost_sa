# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
from kafka import KafkaProducer, KafkaConsumer
import json
from configs import kafka
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)


# meta_class = dict()


# class kafka_helper():
#     __instance = None

#     def __init__(self):
#         # self.producer = KafkaProducer(
#         #     bootstrap_servers=kafka.bootstrap_servers)
#         pass

#     def __new__(cls, *args, **kwargs):
#         if cls.__instance is None:
#             cls.__instance = super(kafka_helper, cls).__new__(
#                 cls, *args, **kwargs)
#         return cls.__instance

#     def insert_test(self, msg):
#         # self.producer = KafkaProducer(
#         #     bootstrap_servers=kafka.bootstrap_servers)

#         # if not self.producer.bootstrap_connected():
#         #     self.producer = KafkaProducer(
#         #         bootstrap_servers=kafka.bootstrap_servers)
#         # feature = self.producer.send(topic=kafka.kafka_topic, value=json.dumps(msg).encode())
#         # self.producer.flush() 
#         # sta = feature.get(timeout=10)
#         # print(1111111111111,sta)
#         # self.producer.close()
#         __kafka_client = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
#         __kafka_client.send(kafka.kafka_topic, json.dumps(msg))#.add_callback(on_kafka_send_success).add_errback(on_kafka_send_error)
#         __kafka_client.flush()

# producer = KafkaProducer(
#             bootstrap_servers=kafka.bootstrap_servers)

producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
def insert_message_to_kafka(msg):
    # global producer
    # msg = {'e':'f'}
    # msg = json.dumps(msg)
    # producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
    # for i in range(10):
    #     print(producer.bootstrap_connected())
    # kh=kafka_helper()
    # kh.insert_test(msg)
    # producer = kh.producer
    # if not producer.bootstrap_connected():
    #     producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)
    # #     print('no')
    # # elif producer.bootstrap_connected() is True:
    # #     print('yes')
    producer.send(topic=kafka.kafka_topic,value=json.dumps(msg).encode())
    # producer.close()
    # print(2,producer.bootstrap_connected)

def get_message_from_kafka():
    consumer=KafkaConsumer(
        kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id)
    return consumer
    # for msg in consumer:
    #     print(msg)

if __name__ == "__main__":
    insert_message_to_kafka(msg={'msg': 'test'})
    # get_message_from_kafka()
