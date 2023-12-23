import bz2
import json
import os
from client import get_producer, DEFAULT_TOPIC, produce_msg, send_msg
import time
directory = 'data'


def main():
    counter = 0
    measurements = []
    counter2 = 0
    tic = time.perf_counter
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)
        with bz2.open(f) as bzinput:
            for i, line in enumerate(bzinput):
                tweets = json.loads(line)
                print(tweets['data']['created_at'], tweets['data']['text'])
                send_msg(key = tweets['data']['created_at'], value = tweets['data']['text'], topic = "INGESTION_TWEETS", producer = get_producer())   
                counter += 1
                if counter == 100 & counter2 < 11:
                    toc = time.perf_counter
                    measurements.append[tic-toc]
                    tic = time.perf_counter
                    counter = 0
                    counter2 += 1
                if counter == 100 & counter2 >= 11:
                    print(measurements)

if __name__ == "__main__":
    main()
