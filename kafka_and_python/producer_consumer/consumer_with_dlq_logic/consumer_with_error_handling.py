"""
    A Kafka consumer that consumes messages in JSON format from json-topic.
    If the message is malformed i.e. the message is not in valid JSON format then the consumer does not stop.
    It reads that error message and moves it to another DLQ topic: json-topic-dlq.
    Where as, if the message is correct it is moved to the valid messages topic after transformation: json-topic-2.
"""

import json
import traceback
from kafka import KafkaConsumer
from kafka import KafkaProducer
from config import *

# Creating the Kafka producer for valid messages
target_topic = 'json-topic-2'
json_serializer = lambda x: json.dumps(x).encode('utf-8')
valid_producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS],
                               value_serializer=json_serializer,
                               acks='all')

# Creating the Kafka producer for invalid/malformed messages
dlq_topic = 'json-topic-dlq'
string_serializer = lambda x: x.encode('utf-8')
dlq_producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS],
                             value_serializer=string_serializer,
                             acks='all')

# Creating the Kafka consumer
source_topic = 'json-topic'
consumer = KafkaConsumer(source_topic, group_id='some_consumer_group',
                         bootstrap_servers=[BOOTSTRAP_SERVERS],
                         auto_offset_reset='latest',
                         consumer_timeout_ms=100000)

while True:
    msg_pack = consumer.poll(timeout_ms=500)  # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
    for tp, messages in msg_pack.items():
        for message in messages:

            data = message.value.decode('utf-8')
            print("\nConsumed[%s/%d] %d: key=%s value=%s" % (message.topic, message.partition,
                                                           message.offset, message.key,
                                                           message.value))
            try:
                json_data = json.loads(data)

                transformed_employee_number = 'EMP-'+str(json_data['Employee-Number'])
                print("Transforming Employee-Number:", json_data['Employee-Number'],
                      'to Employee-Number:', transformed_employee_number)

                json_data['Employee-Number'] = transformed_employee_number
                print("Sending json data to valid topic: ", json_data)

                valid_producer.send(topic=target_topic, value=json_data).get()
                print("Successfully send json data to valid topic: ", json_data)

            except json.decoder.JSONDecodeError as e:
                print(e.__class__.__name__, e)
                print("Sending malformed json data to DLQ topic: ", data)
                dlq_producer.send(topic=dlq_topic, value=data).get()
                print("Successfully sent malformed json data to DLQ topic: ", data)
