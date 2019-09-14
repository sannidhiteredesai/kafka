from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
from config import *

new_topic = "mytopic"
admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
new_topics = [NewTopic(name=new_topic, num_partitions=3, replication_factor=1)]

existing_topics = KafkaConsumer(bootstrap_servers=[BOOTSTRAP_SERVERS]).topics()
if new_topic in existing_topics:
    print('Topic:', new_topic, 'already exists')

else:
    admin_client.create_topics(new_topics=new_topics, validate_only=False)
    print('Topic:', new_topic, 'created successfully')
