# List, describe, delete the consumer groups

### List all consumer groups
bash-4.4# kafka-consumer-groups.sh  --bootstrap-server localhost:9092 --list
some_consumer_group

### Delete consumer group
bash-4.4# kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group some_consumer_group
Deletion of requested consumer groups ('some_consumer_group') was successful.


### Describe all consmer groups
kafka-consumer-groups.sh  --bootstrap-server localhost:9092 --describe --all-groups
(Output similar to below commands)

### Describe single consumer group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group some_consumer_group --describe
(Output similar to below commands)

### List all topics that a consumer group is consuming from with offsets and lag - when consumers are active
bash-4.4# kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group some_consumer_group --describe

| GROUP | TOPIC | PARTITION | CURRENT-OFFSET | LOG-END-OFFSET | LAG | CONSUMER-ID | HOST | CLIENT-ID |
| ------ | ------ | ------- | -------------- | -------------- | -- | -- | -- | -- |
|some_consumer_group |json-topic | 0 | 20 | 20 | 0| kafka-python-1.4.6-fa73d85c-1f44-4c0c-bfdc-637f8a0b26ad | /10.255.0.2 | kafka-python-1.4.6 |
|some_consumer_group |json-topic | 1 | 26 | 26 | 0| kafka-python-1.4.6-fa73d85c-1f44-4c0c-bfdc-637f8a0b26ad | /10.255.0.2 | kafka-python-1.4.6 |
|some_consumer_group |json-topic | 2 | 36 | 36 | 0| kafka-python-1.4.6-fa73d85c-1f44-4c0c-bfdc-637f8a0b26ad | /10.255.0.2 | kafka-python-1.4.6 |

### List all topics that a consumer group is consuming from with offsets and lag - when consumers are inactive
bash-4.4# kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group some_consumer_group --describe
Consumer group 'some_consumer_group' has no active members.

| GROUP | TOPIC | PARTITION | CURRENT-OFFSET | LOG-END-OFFSET | LAG | CONSUMER-ID | HOST | CLIENT-ID |
| - | - | - | - | - | - | - | - | - |
| some_consumer_group | json-topic | 0 | 20 | 20 | 0 | - | - | - |
| some_consumer_group | json-topic | 1 | 26 | 26 | 0 | - | - | - |
| some_consumer_group | json-topic | 2 | 36 | 36 | 0 | - | - | - |


# Reset consumer group offsets to earliest

### Only list the new offsets without actually doing so
bash-4.4# kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group some_consumer_group --reset-offsets --to-earliest --topic json-topic
WARN: No action will be performed as the --execute option is missing.In a future major release, the default behavior of this command will be to prompt the user before executing the reset rather than doing a dry run. You should add the --dry-run option explicitly if you are scripting this command and want to keep the current default behavior without prompting.

| GROUP | TOPIC | PARTITION | NEW-OFFSET |
| - | - | - | - |
| some_consumer_group | json-topic | 0 | 0 |
| some_consumer_group | json-topic | 2 | 0 |
| some_consumer_group | json-topic | 1 | 0 |


### Reset consumer group offsets to earliest
bash-4.4# kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group some_consumer_group --reset-offsets --to-earliest --topic json-topic --execute

| GROUP | TOPIC | PARTITION | NEW-OFFSET |
| - | - | - | - |
| some_consumer_group | json-topic | 0 | 0 |
| some_consumer_group | json-topic | 2 | 0 |
| some_consumer_group | json-topic | 1 | 0 |

### Some notes taken from [here](https://gist.github.com/marwei/cd40657c481f94ebe273ecc16601674b#note)
 - The consumer group must have no running instance when performing the reset. Otherwise the reset will be rejected.
 - There are many other resetting options, run kafka-consumer-groups for details
   - --shift-by <positive_or_negative_integer>
   - --to-current
   - --to-latest
   - --to-offset <offset_integer> (If latest offset = 20 and we give --to-offset 40, then it automatically resets to 20)
   - --to-datetime <datetime_string>
   - --by-duration <duration_string>
 - The command also provides an option to reset offsets for all topics the consumer group subscribes to: --all-topics