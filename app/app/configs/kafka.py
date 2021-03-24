#kafka_server

bootstrap_servers=['your_server_domain_here:9092'] #Kafka服务器的地址
client_group_id='your_group_id_here' #Kafka群组地址，同一群组共享一个Offset，不会重复，也不会漏。
kafka_topic='your_topic_here' #Kafka的Topic