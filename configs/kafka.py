# -*- coding: utf-8 -*-
#
#Date: 2022-10-06 16:15:40
#Author: unknowwhite@outlook.com
#WeChat: Ben_Xiaobai
#LastEditTime: 2025-06-01 20:26:54
#FilePath: \ghost_sa_github_cgq\configs\kafka.py
#
import sys
sys.path.append('./')
#kafka_server

bootstrap_servers=['192.168.193.60:9092'] #Kafka服务器的地址
client_group_id='ghost_sa_cgq' #Kafka群组地址，同一群组共享一个Offset，不会重复，也不会漏。
kafka_topic='ghost_sa' #Kafka的Topic
client_id = 'get_message_from_kafka'
kafka_offset_reset = 'latest' #latest,earliest,none