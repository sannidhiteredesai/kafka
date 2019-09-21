# Learn Kafka

This project will provide the basic code snippets for interacting with Kafka in following different laungauges:
  - Python
  - Java (...will be available soon)

### Kafka Setup
Here I have setup Kafka using docker. The docker file can be found here: [docker-kafka-stack.yml](https://github.com/sannidhiteredesai/kafka/blob/master/docker_files/docker-kafka-stack.yml)
This uses the wurstmeister/zookeeper image for zookeeper and wurstmeister/kafka image for kafka and start 1 container instance each for zookeeper and kafka. Some volumes are also used to persist the topics and messages even if the containers are restarted.

> You can also setup your own standalone Kafka cluster instead of using docker. The instructions for that can be found on [Kafka's official website](https://kafka.apache.org/quickstart)

In whichever approach you use you can even try to scale up the cluster by using more than one broker. Here we will be using only one broker as this should be fine in development environment.


### Kafka Apis
We will be using the kafka-python package here and primarliy focus on:
1. [Topics](https://github.com/sannidhiteredesai/kafka/tree/master/kafka_and_python/topics) - Includes apis to list/create/delete topics using Python
2. [Producer-Consumer](https://github.com/sannidhiteredesai/kafka/tree/master/kafka_and_python/producer_consumer) - Writing producers and consumers in Python


### Serde (Serializer-Deserializer)
Kafka only supports sending messages in form of bytes. So to convert our complex objects into bytes we need a serializer and to construct back the object from bytes we need deserializer.
**Serde** = **Ser**ializer + **De**serializer

The different Serde's which we will be using here are:
  - [String Serde](https://github.com/sannidhiteredesai/kafka/tree/master/kafka_and_python/producer_consumer/serde/string_serde)
  - [Json Serde](https://github.com/sannidhiteredesai/kafka/tree/master/kafka_and_python/producer_consumer/serde/json_serde)

### Example message format
In project we take the example of sending the following data to kafka topic:
> < Employee Id > < Employee Name > < Employee Salary >

We will see how the same information when stored as string/avro/json/... is converted to bytes to sent to kafka.

### Handling error messages with DLQ
Let's say we have a Kafka consumer that consumes JSON messages from a source topic. But due to some reason one of the JSON messages on source topic is malformed. This will lead to an exception when the consumer tries to decode the bytes from source topic as JSON. To handle such a scenario weuse DLQs (Dead Letter Queues) and send the malformed JSON messages to DLQ so that the consumer does not stop because of malformed JSONs. The implementation for that can be found [here](https://github.com/sannidhiteredesai/kafka/tree/master/kafka_and_python/producer_consumer/consumer_with_dlq_logic/consumer_with_error_handling.py)
