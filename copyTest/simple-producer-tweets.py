import bz2
import json
import os
from client import get_producer, DEFAULT_TOPIC, produce_msg, send_msg
directory = 'data'

def main():
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)
        with bz2.open(f) as bzinput:
            for i, line in enumerate(bzinput):
                tweets = json.loads(line)
                send_msg(key = tweets['data']['created_at'], value = tweets['data']['text'], topic = "INGESTION_TWEETS", producer = get_producer())   

if __name__ == "__main__":
    main()
