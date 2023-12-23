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
        rows = []
        counter = 0
        filename = "persistentTweets.csv"
        # Print a list of the data"
        for x in list(reader):
                print(x)
                #x["temperature"] = x["temperature"].replace('"', '')
                row = [x["creation_timestamp"]]
                rows.append(row)
        print (os.path.exists(filename))
        with open(filename, 'w') as csvfile: 
                csvwriter = csv.writer(csvfile)
                if (os.path.exists(filename) != True):
                        header = ['date']
                        csvwriter.writerow(header) 
                        print("added headertweets")
                for row in rows:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(row) 
                csvfile.close()
                

