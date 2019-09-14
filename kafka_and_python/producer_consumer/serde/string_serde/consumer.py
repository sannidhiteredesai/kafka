from kafka import KafkaConsumer
from config import *

topic='mytopic'
string_deserializer = lambda x: x.decode('utf-8')

# auto_offset_reset='earliest' will be used only for the first time when no messages have been
# consumed yet using the given consumer group.
# For the next consumptions the offset wil have been committed so the value of auto_offset_reset is not used
consumer = KafkaConsumer(topic, group_id='some_consumer_group',
                         bootstrap_servers=[BOOTSTRAP_SERVERS],
                         value_deserializer=string_deserializer,
                         auto_offset_reset='earliest')

# This for loop will continuously wait for new messages
for msg in consumer:
    print (msg)
