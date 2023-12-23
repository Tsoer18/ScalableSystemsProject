from kafka import KafkaProducer, KafkaConsumer
import json
from data_model import generate_sample, PackageObj
from hdfs.ext.avro import AvroWriter, AvroReader
from HDFSclient import get_hdfs_client
import re
import csv
import os


client = get_hdfs_client()
with AvroReader(client, "/weather-report.avro") as reader:
        
        counter = 0
        # Print a list of the data
        for x in list(reader):
                y = json.loads(x)
                print(y[date])
                print(y[temperature])
                print(counter)
        

