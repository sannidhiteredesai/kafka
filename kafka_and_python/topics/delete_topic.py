from kafka.admin import KafkaAdminClient
from kafka import KafkaConsumer
from config import *

delete_topic = "mytopic"
admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
consumer = KafkaConsumer(bootstrap_servers=[BOOTSTRAP_SERVERS])

if delete_topic in consumer.topics():
    admin_client.delete_topics(topics=[delete_topic])

    if delete_topic not in consumer.topics():
        print(f"Topic: {delete_topic} deleted successfully !!")
    else:
        print(f"Unable to delete topic: {delete_topic}")

else:
    print(f"Topic: {delete_topic} not found !!")

consumer.close()
admin_client.close()