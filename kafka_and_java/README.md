# Kafka Producer and Consumer

This is the example of basic Kafka producer and consumer using string serde.

When producer is executed the output is:
```
Sent message :1
Sent message :2
Sent message :3
Sent message :4
Sent message :5
Sent message :6
Sent message :7
Sent message :8
Sent message :9
Sent message :10
```
When consumer is executed the output is:
(In the case of consumer the ordering of numbers varies as the consumer reads from multiple topic partitons)
```
Consumed: 2
Consumed: 5
Consumed: 8
Consumed: 3
Consumed: 6
Consumed: 9
Consumed: 1
Consumed: 4
Consumed: 7
Consumed: 10
```


### Link
Please check the [link](http://blog.empeccableweb.com/wp/2016/11/30/kafka-producer-and-consumer-example/) which shows how to gracefully shutdown the producer and consumer using user input.