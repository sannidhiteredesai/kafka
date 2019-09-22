NOTES:
##### Major companies using Kafka
- LinkedIn
- Uber
- Netflix
- Spotify

##### What is Kafka ?
Apache Kafka is an open-source distributed stream-processing software platform developed by LinkedIn and donated to the Apache Software Foundation, written in Scala and Java.

##### Why use kafka and some use cases ?
- Provides replication
- Producer vs consumer speed difference is handled
- Commit log + replay feature
- Fault tolerant - If broker fails, if consumer fails, if new partition is added
- Log aggregation
- Click stream analysis to show targeted adds

##### Kafka Architecture
Major Components in the architecture are:
- Broker
- Topic
- Partitions

##### Controller/Leader/Follower
- Controller: Maintains the Kafka administration tasks.
- Leader: Broker on which a particular partition's main replica is written.
- Follower: Other brokers which follow the main partition and replicate messages.

##### Does kafka buffer any messages ?
Yes on producer as well as consumer side.

##### Why is Zookeeper needed in Kakfa ?
- It mananges all the brokers in cluster.
- Used for controller election.

##### Why controller is needed in Kafka ?
- It accepts requests from a kafka consumer and provides all the consumer group specific offsets to it.
- When a partition leader fails, it finds a new healthy in-sync broker for each partition and then elects them as leader.

##### Can we increase or decrease the number of partitions in a kafka topic ?
We can only increase the number of partitions and cannot decrease it.

##### Will adding new partitions redistribute the existing data ?
No the existing data will remain as it is.

##### What does replication factor of 3 mean in kafka ?
It means 1 leader partition + 2 follower partitions.

##### Where are consumer offsets stored by Kafka ?
When the group coordinator receives an OffsetCommitRequest, it appends the request to a special "compacted" Kafka topic named __consumer_offsets.

##### How are old messaged deleted ?
Data is deleted one log segment at a time. The log manager allows pluggable delete policies to choose which files are eligible for deletion. The current policy deletes any log with a modification time of more than N days ago.

##### Log retention
When the log is cleaned up it is done segment wise, so for each closed segement file if the last message is older then 7 days then that log segment is cleaned up.

##### When does consumer rebalance occur ?
- If a consumer from a consumer groups dies then another consumer reads from the partition the other consumer was reading.
- When a new consumer is online it balances the partitons only if another consumer is overloaded.
- When a new partiton is created, an existing consumer starts reading from the new partition also.

##### Message delivery - atleast/atmost/exactly once
Good documentation links:
- https://kafka.apache.org/documentation/#semantics
- https://hevodata.com/blog/kafka-exactly-once/

##### What happens when a new broker is added to the cluster ?
Nothing happens automatically. Manually a command needs to be executed to mark this broker as leader for one of the partitions and then Kafka will add the new server as a follower of the partition it is migrating from an existing server and allow it to fully replicate the existing data in that partition. When the new server has fully replicated the contents of this partition and joined the in-sync replica one of the existing replicas will delete their partition's data.

##### Can you pause and resume consumers ?
Yes - Pause will not cause rebalance even though poll is not run for some iterations.

##### Kafka vs Flume
Taken from: https://www.linkedin.com/pulse/flume-kafka-real-time-event-processing-lan-jiang/

Compared to Flume, Kafka wins on the its superb scalability and messsage durablity.

Kafka is very scalable. One of the key benefits of Kafka is that it is very easy to add large number of consumers without affecting performance and without down time. That's because Kafka does not track which messages in the topic have been consumed by consumers. It simply keeps all messages in the topic within a configurable period. It is the consumers' responsibility to do the tracking through offset. In contrast, adding more consumers to Flume means changing the topology of Flume pipeline design, replicating the channel to deliver the messages to a new sink. It is not really a scalable solution when you have huge number of consumers. Also since the flume topology needs to be changed, it requires some down time.

Kafka's scalability is also demonstrated by its ability to handle spike of the events. This is where Kakfa truly shines because it acts as a "shock absorber" between the producers and consumers. Kafka can handle events at 100k+ per second rate coming from producers. Because Kafka consumers pull data from the topic, different consumers can consume the messages at different pace. Kafka also supports different consumption model. You can have one consumer processing the messages at real-time and another consumer processing the messages in batch mode. On the contrary, Flume sink supports push model. When event producers suddenly generate a flood of messages, even though flume channel somewhat acts as a buffer between source and sink, the sink endpoints might still be overwhelmed by the write operations.

Message durability is also an important consideration. Flume supports both ephemeral memory-based channel and durable file-based channel. Even when you use a durable file-based channel, any event stored in a channel not yet written to a sink will be unavailable until the agent is recovered. Moreoever, the file-based channel does not replicate event data to a different node. It totally depends on the durability of the storage it writes upon. If message durability is crucial, it is recommended to use SAN or RAID. Kafka supports both synchronous and asynchronous replication based on your durability requirement and it uses commodity hard drive.

Flume does have some features that makes it attractive to be a data ingestion and simple event processing framework. The key benefit of Flume is that it supports many built-in sources and sinks, which you can use out of box. If you use Kafka, most likely you have to write your own producer and consumer. Of course, as Kakfa becomes more and more popular, other frameworks are constantly adding integration support for Kafka. For example, Apache Storm added Kafka Spout in release 0.9.2, allowing Storm topology to consume data from Kafka 0.8.x directly.

Kafka does not provider native support for message processing. So mostly likely it needs to integrate with other event processing frameworks such as Apache Storm to complete the job. In contrast, Flume supports different data flow models and interceptors chaining, which makes event filtering and transforming very easy. For example, you can filter out messages that you are not interested in the pipeline first before sending it through the network for obvious performance reason. However, It is not suitable for complex event processing, which I will address in a future post.

The good news is that the latest trend is to use both together to get the best of both worlds. For example, Flume in CDH 5.2 starts to accept data from Kafka via the KafkaSource and push to Kafka using the KafkaSink. Also CDH 5.3 (the latest release) adds Kafka Channel support, which addresses the event durability issue mentioned above.

So in all:
- Kafka - Fault tolerant (data is replicated), efficient in case of increasing consumers(as kafka uses pull based approach i.e. kafka consumers pull data), performant if input load suddenly increases.
- Flume - Supports more connector out of the box. Flume uses push based approach.

##### Maximum size of kafka message
1MB

##### Message format Kafka:
https://kafka.apache.org/documentation/#messageformat
A log for a topic named "my_topic" with two partitions consists of two directories (namely my_topic_0 and my_topic_1) populated with data files containing the messages for that topic. The format of the log files is a sequence of "log entries""; each log entry is a 4 byte integer N storing the message length which is followed by the N message bytes. Each message is uniquely identified by a 64-bit integer offset giving the byte position of the start of this message in the stream of all messages ever sent to that topic on that partition. The on-disk format of each message is given below. Each log file is named with the offset of the first message it contains. So the first file created will be 00000000000.kafka, and each additional file will have an integer name roughly S bytes from the previous file where S is the max log file size given in the configuration.

##### Kafka consumer offset max value?
https://stackoverflow.com/questions/34408970/kafka-consumer-offset-max-value
Offset value is not rolled back at this moment whenever the older logs are cleaned up. Since the offset is a long, it can last for a really long time. If you write 1TB a day, you can keep going for about 4 million days. Plus, you can always use more partitions (each partition has its own offset).

##### Key and Timestamp in Kafka Message:
https://kafka.apache.org/0102/javadoc/org/apache/kafka/clients/producer/ProducerRecord.html
A key/value pair to be sent to Kafka. This consists of a topic name to which the record is being sent, an optional partition number, and an optional key and value.
If a valid partition number is specified that partition will be used when sending the record. If no partition is specified but a key is present a partition will be chosen using a hash of the key. If neither key nor partition is present a partition will be assigned in a round-robin fashion.
The record also has an associated timestamp. If the user did not provide a timestamp, the producer will stamp the record with its current time. The timestamp eventually used by Kafka depends on the timestamp type configured for the topic.

##### Delete topic vs compaction topics
Retention policy is to delete all the old topic by default. But if retention policy is set to compact then the if a new message with same key comes then the old message with same key will be marked as deleted.

##### Confluent vs Apache kafka
Provides following that is different than the original Apache Kafka distribution:
- REST API
- Schema Registry
- KSQL
- Many connectors for Kafka Connect

##### Kafka Connect
- https://data-flair.training/blogs/kafka-connect/
- Example: https://www.tutorialkart.com/apache-kafka/apache-kafka-connector/

##### Kafka Streams
- https://data-flair.training/blogs/kafka-streams/
- Example: https://dzone.com/articles/kafka-streams-more-than-just-dumb-storage

##### KSQL
- https://docs.confluent.io/current/ksql/docs/index.html
