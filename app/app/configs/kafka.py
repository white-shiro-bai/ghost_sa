#kafka_server

bootstrap_servers=['172.18.5.15:9092', '172.18.5.16:9092', '172.18.5.17:9092'] #Kafka服务器的地址
client_group_id='events-tracking' #Kafka群组地址，同一群组共享一个Offset，不会重复，也不会漏。
kafka_topic='events_tracking' #Kafka的Topic
