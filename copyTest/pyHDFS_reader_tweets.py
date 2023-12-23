from kafka import KafkaProducer, KafkaConsumer
import json
from data_model import generate_sample, PackageObj
from hdfs.ext.avro import AvroWriter, AvroReader
from HDFSclient import get_hdfs_client
import re
import csv
import os

client = get_hdfs_client()
with AvroReader(client, "/tweets.avro") as reader:
        schema = reader.schema  # The inferred schema.
        # content = reader.content  # The remote file's HDFS content object.

        # Print the inferred schema
        print(schema)
        print("\n")
        counter = 0
        # Print a list of the data
        for x in list(reader):
                print(x)
                counter += 1
                print(counter)
        

