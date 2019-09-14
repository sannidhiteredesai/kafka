from kafka.admin import KafkaAdminClient
from kafka import KafkaConsumer
from config import *

delete_topic = "mytopic"
admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
admin_client.delete_topics(topics=[delete_topic])

topics = KafkaConsumer(bootstrap_servers=[BOOTSTRAP_SERVERS]).topics()
if delete_topic not in topics:
    print(f"Topic: {delete_topic} deleted successfully !!")
else:
    print(f"Unable to delete topic: {delete_topic}")