# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from kafka import KafkaProducer, KafkaConsumer
import json
from app.configs import kafka
from app.configs import admin


class Single(object):
    """单例模式"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            if hasattr(cls, "initialize"):
                cls._instance.initialize(*args, **kwargs)
        return cls._instance


class MsgQueue(Single):
    """
    这个整成单例模式是因为：uwsgi配合kafka-python在多进程下会有问题，这里希望每个进程单独享有一个kafka producer实例,
    也就是说当初始化app对象后，并不会生成producer实例，而是在运行时再生成，
    具体参考：https://github.com/dpkp/kafka-python/issues/721
    """
    app = None

    def initialize(self):
        self.producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers,
                                      compression_type='gzip')

    def send(self, key, msg):
        """
        :param key: msg key
        :param msg:
        :return:
        """
        if isinstance(key, str):
            key = key.encode()
        try:
            future = self.producer.send(topic=kafka.kafka_topic, key=key, value=json.dumps(msg).encode())
            result = future.get(timeout=10)
        except Exception as e:
            print('发送失败: {}'.format(e))


def insert_message_to_kafka(key, msg):
    # 若配置使用kafka，不操作
    if not admin.use_kafka:
        return False

    # 多进程支持
    MsgQueue().send(key, msg)


kafka_offset_reset = 'earliest' #latest,earliest,none 首次拉取kafka订阅的模式


def get_message_from_kafka():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka')
    return consumer

def get_message_from_kafka_independent_listener():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=admin.independent_listener_kafka_client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka_independent_listener')
    return consumer

if __name__ == "__main__":
    insert_message_to_kafka(key='123231231', msg={'msg': 'test'})