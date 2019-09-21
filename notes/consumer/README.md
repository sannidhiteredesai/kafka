# Graceful shutdown of consumer

### You may need to shutdown the kafka consumer in following cases:
 - In development/testing environment the consumer should be run for only some messages and then must be shutdown.
 - In production environment when the new version of kafka consumer code needs to be deployed, so the existing consumer will be shutdown and then rerun using new code.

### In such a case how to implement a kafka consumer ?
Run the consumer in a separate thread and the main thread can monitor any signals to shutdown the consumer.
The signal can be:
 - Calling some rest end point
 - Some marker file in a directory

A good example of how the consumer can be shutdown based on user input is given (here)[http://blog.empeccableweb.com/wp/2016/11/30/kafka-producer-and-consumer-example/].
