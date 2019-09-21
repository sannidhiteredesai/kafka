from kafka import KafkaConsumer, TopicPartition
from config import *

string_deserializer = lambda x: x.decode('utf-8')


#################### Using seek_to_end() ###################

# Don't give topic name while creating the consumer, instead use assign method as below
consumer = KafkaConsumer(group_id='some_consumer_group',
                         bootstrap_servers=[BOOTSTRAP_SERVERS],
                         value_deserializer=string_deserializer,
                         auto_offset_reset='latest',
                         consumer_timeout_ms=100000)

partition0 = TopicPartition('string-topic', 0)
partition1 = TopicPartition('string-topic', 1)
partition2 = TopicPartition('string-topic', 2)
consumer.assign([partition0, partition1, partition2])

# Assume the consumer has NOT consumed all messages from all partitions.
# But after the below method is executed offset will be reset to end for all the partitions.
consumer.seek_to_end()

for msg in consumer:
    print("Consumed[%s-%d] %d: key=%s value=%s" % (msg.topic, msg.partition,
                                         msg.offset, msg.key,
                                         msg.value))
