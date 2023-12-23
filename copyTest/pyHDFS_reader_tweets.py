from kafka import KafkaProducer, KafkaConsumer
import json
from data_model import generate_sample, PackageObj
from hdfs.ext.avro import AvroWriter, AvroReader
from HDFSclient import get_hdfs_client
import re
import csv
import os
import time

while(True):
        client = get_hdfs_client()
        with AvroReader(client, "/tweets.avro") as reader:
                rows = []
                counter = 0
                filename = "persistentTweets.csv"
                # Print a list of the data"
                for x in list(reader):
                        print(x)
                        row = [x["creation_timestamp"]]
                        rows.append(row)
                fileExists = os.path.exists(filename)
                with open(filename, 'w') as csvfile: 
                        csvwriter = csv.writer(csvfile)
                        if (fileExists == False):
                                header = ["date"]
                                csvwriter.writerow(header) 
                                print("added headertweets")
                        for row in rows:
                                csvwriter.writerow(row)
                                counter += 1
                        print("Wrote csv file with all tweet data with this many rows:")
                        print(counter)
                        print("__________________________")
                        csvfile.close()
        time.sleep(60)
                

