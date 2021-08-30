
# kafka_server
bootstrap_servers=['172.18.5.17:9092'] #Kafka服务器的地址
client_group_id='your_group_id_here' #Kafka群组地址，同一群组共享一个Offset，不会重复，也不会漏。
kafka_topic='your_topic_here' #Kafka的Topic
client_id = 'get_message_from_kafka'
kafka_offset_reset = 'latest' #latest,earliest,none
