from kafka import KafkaConsumer
from config import *

topic='string-topic'
string_deserializer = lambda x: x.decode('utf-8')

# auto_offset_reset will be used only for the first time when no messages have been
# consumed yet using the consumer in consumer group.
# For the next consumptions the offset will have been committed so the value of auto_offset_reset is not used
# StopIteration if no message after 100secs by using consumer_timeout_ms=100000
consumer = KafkaConsumer(topic, group_id='some_consumer_group',
                         bootstrap_servers=[BOOTSTRAP_SERVERS],
                         value_deserializer=string_deserializer,
                         auto_offset_reset='latest',
                         consumer_timeout_ms=100000)

# This for loop will continuously wait for new messages
for msg in consumer:
    print("Consumed[%s-%d] %d: key=%s value=%s" % (msg.topic, msg.partition,
                                         msg.offset, msg.key,
                                         msg.value))
