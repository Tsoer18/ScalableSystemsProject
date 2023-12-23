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
        rows = []
        counter = 0
        filename = "persistentTemperature.csv"
        # Print a list of the data"     
        for x in list(reader):
                x["temperature"] = x["temperature"].replace('"', '')
                row = [x["date"], x["temperature"]]
                rows.append(row)
        fileExists =os.path.exists(filename)
        with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                if (fileExists == False):
                        header = ['date','temperature']
                        csvwriter.writerow(header) 
                        print('added header')
                for row in rows:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(row) 
                csvfile.close()
        

