from kafka import KafkaProducer, KafkaConsumer
import json
from data_model import generate_sample, PackageObj
from hdfs.ext.avro import AvroWriter, AvroReader
from HDFSclient import get_hdfs_client
import re
import csv
import os
import os.path
import time



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
    
    client = get_hdfs_client()
    for msg in consumer:
        #print(PackageObj(**json.loads(msg.value.decode(DEFAULT_ENCODING))))        
        if avro_file_path == "/weather-report.avro":
            with AvroWriter(client, avro_file_path,overwrite=True) as writer:
                with AvroReader(client, "/weather-report.avro") as reader:
                    listReader = list(reader)
                    for data in listReader:
                        writer.write(data)
                writer.write({"date": msg.key.decode(DEFAULT_ENCODING), "temperature" : msg.value.decode(DEFAULT_ENCODING)})
                print("Wrote the following to hdfs:")
                print(msg.key.decode(DEFAULT_ENCODING))
                print(msg.value.decode(DEFAULT_ENCODING))
                print("_____________________")
        if avro_file_path == "/tweets.avro":
            
            message_value = msg.value.decode(DEFAULT_ENCODING)
            if (search(message_value) != None):
                print("Found tweet with value:")
                print(message_value)
                print("____________________")
                with AvroWriter(client, avro_file_path,overwrite=True) as writer:
                        with AvroReader(client, "/tweets.avro") as reader:
                            listReader = list(reader)
                            for data in listReader:
                                writer.write(data)
                        writer.write({"creation_timestamp": msg.key.decode(DEFAULT_ENCODING)})
                print("Wrote the following to hdfs:")
                print(msg.key.decode(DEFAULT_ENCODING))
                
                print("_____________________")
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
    rows = []
    for msg in consumer:
        if counter < 100:
            key = msg.key.decode(DEFAULT_ENCODING)
            value = msg.value.decode(DEFAULT_ENCODING)
            counter_string = str(counter)
            print("Current counter: " + counter_string)
            value = value.replace('"', '')
            row = [key, value]
            rows.append(row)
            counter += 1
        else:
            if (os.path.isfile(filename)):
                os.remove(filename)
            with open(filename, 'w') as csvfile: 
                csvwriter = csv.writer(csvfile)
                header = ["date", "temperature"]
                csvwriter.writerow(header)
                for row in rows:
                    csvwriter.writerow(row) 
                csvfile.close()   
            print("Wrote rows to file")
            counter = 0
            rows = []
def receive_msg_tweets(consumer: KafkaConsumer) -> None:
    counter = 0
    filename = "tweets.csv"
    rows = []
    for msg in consumer:
        if counter < 100:
            message_value = msg.value.decode(DEFAULT_ENCODING)
            if (search(message_value) != None):
                print("Found tweet with value:")
                print(message_value)
                print("____________________")
                key = msg.key.decode(DEFAULT_ENCODING)
                counter_string = str(counter)
                row = [key]
                rows.append(row)
                counter += 1
        else:
            if (os.path.isfile(filename)):
                os.remove(filename)
            with open(filename, 'w') as csvfile: 
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["date"])    
                for row in rows:
                    csvwriter.writerow(row) 
                csvfile.close()   
            print("Wrote rows to file")
            counter = 0
            rows = []
def search(value):
    
    words = ["climate", "global warming", "temperature"]
    tic = time.perf_counter()
    for word in words:
        if (re.search(word,value) != None):
            toc = time.perf_counter()
            return 'found mention'
    toc = time.perf_counter()

    print((toc-tic)*100)

    return None

    