from kafka import KafkaConsumer
from config import *

topics = KafkaConsumer(group_id='test', bootstrap_servers=[BOOTSTRAP_SERVERS]).topics()
if topics:
    print('Topics: ', topics)
else:
    print('No topics found !!')
