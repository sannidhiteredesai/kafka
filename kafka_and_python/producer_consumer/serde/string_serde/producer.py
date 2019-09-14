"""
Kafka producer to send employee details in String serialized format
"""

from kafka import KafkaProducer
from config import *

topic = 'mytopic'
string_serializer = lambda x: x.encode('utf-8')
producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS], value_serializer=string_serializer)

for i in range(1, 11):
    emp_no = i
    emp_name = f'Name-{i}'
    emp_salary = i * 10
    message = f'{emp_no},{emp_name},{emp_salary}'
    print(f'Sending message: {message}')
    producer.send(topic=topic, value=message)

# As producer.send() is asynchronous by default we use producer.flush() to wait until all the buffered messages are sent
producer.flush()
