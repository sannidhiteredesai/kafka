"""
Kafka producer to send employee details in Json serialized format like:
{
    "Employee-Number": <Number>,
    "Employee-Name": "<Name>",
    "Employee-Salary": <Salary>,
}
"""

from kafka import KafkaProducer
from config import *
import json

topic = 'json-topic'
json_serializer = lambda x: json.dumps(x).encode('utf-8')
producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS],
                         value_serializer=json_serializer)

for i in range(1, 11):
    message = {
        "Employee-Number": i,
        "Employee-Name": f'Name-{i}',
        "Employee-Salary": i * 10,
    }
    print(f'Sending message: {message}')
    producer.send(topic=topic, value=message)

# As producer.send() is asynchronous by default we use producer.flush() to wait until all the buffered messages are sent
producer.flush()
producer.close()
