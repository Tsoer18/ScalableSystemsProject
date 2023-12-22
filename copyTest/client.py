from kafka import KafkaProducer, KafkaConsumer
import json
from data_model import generate_sample, PackageObj
from hdfs.ext.avro import AvroWriter, AvroReader
from HDFSclient import get_hdfs_client
import re
import csv
import os

KAFKA_BROKERS: str = (
    "strimzi-kafka-bootstrap.kafka:9092"  # <service name>.<namepsace>:<port>
)

DEFAULT_TOPIC: str = "INGESTION"
DEFAULT_ENCODING: str = "utf-8"
DEFAULT_CONSUMER: str = "DEFAULT_CONSUMER"


def get_producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=[KAFKA_BROKERS])


def get_consumer(topic: str, group_id: str = None) -> KafkaConsumer:
    if group_id is None:
        group_id = DEFAULT_CONSUMER
    return KafkaConsumer(topic, bootstrap_servers=[KAFKA_BROKERS], group_id=group_id)


def send_msg(value, key: str, topic: str, producer: KafkaProducer) -> None:
    producer.send(
        topic=topic,
        key=key.encode(DEFAULT_ENCODING),
        value=json.dumps(value).encode(DEFAULT_ENCODING),
    )


def produce_msg(sensor_id: int, topic: str, producer: KafkaProducer) -> None:
    key, value = generate_sample(sensor_id=sensor_id)
    print(value)
    send_msg(key=str(key), value=value, topic=topic, producer=producer)


def recive_msg(consumer: KafkaConsumer, avro_file_path) -> None:
    for msg in consumer:
        #print(PackageObj(**json.loads(msg.value.decode(DEFAULT_ENCODING))))

        client = get_hdfs_client()
        if avro_file_path == "/weather-report.avro":
            with AvroWriter(client, avro_file_path,overwrite=True) as writer:
                writer.write({"date": msg.key.decode(DEFAULT_ENCODING), "temperature" : msg.value.decode(DEFAULT_ENCODING)})
        if avro_file_path == "/tweets.avro":
           with AvroWriter(client, avro_file_path,overwrite=True) as writer:
                #print('happy',re.search(msg.value.decode(DEFAULT_ENCODING)))
                writer.write({"creation_timestamp": msg.key.decode(DEFAULT_ENCODING)})
        #with AvroReader(client, "/weather-report.avro") as reader:
            #schema = reader.schema  # The inferred schema.
            # content = reader.content  # The remote file's HDFS content object.

            # Print the inferred schema
            #print(schema)
            #print("\n")
            # Print a list of the data
            #print(list(reader))

def receive_msg_temperature(consumer: KafkaConsumer) -> None:
    counter = 0
    filename = "temperature.csv"
    print("Received message temperature called...")
    
    for msg in consumer:
        if(counter < 100):
            key = msg.key.decode(DEFAULT_ENCODING)
            value = msg.value.decode(DEFAULT_ENCODING)
            print("Received key: " + key)
            print("Received value:" + value)
            counter_string = str(counter)
            print("Current counter: " + counter_string)
            row = [key, value]
            counter = counter + 1
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row)    
        else:
            os.remove(filename)
            print("Removed file")
            counter = 0