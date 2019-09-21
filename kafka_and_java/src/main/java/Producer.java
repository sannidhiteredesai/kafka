import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import java.util.Properties;
import java.util.Scanner;

public class Producer {
    private static Scanner in;
    public static void main(String[] argv)throws Exception {

        String topicName = "string-topic";

        Properties configProperties = new Properties();
        configProperties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,"192.168.99.101:9092");
        configProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.ByteArraySerializer");
        configProperties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringSerializer");
        configProperties.put(ProducerConfig.ACKS_CONFIG,"all");
        org.apache.kafka.clients.producer.Producer producer = new KafkaProducer(configProperties);

        for(int i=1; i<=10; i++) {
            ProducerRecord<String, String> rec = new ProducerRecord<String, String>(topicName, String.valueOf(i));
            producer.send(rec).get();
            System.out.println("Sent message :"+i);
        }

        producer.close();
    }
}
