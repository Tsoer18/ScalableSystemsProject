import bz2
import json
from client import get_producer, DEFAULT_TOPIC, produce_msg, send_msg


def main():
    with bz2.open('data/0.json.bz2') as bzinput:
        for i, line in enumerate(bzinput):
            tweets = json.loads(line)
            send_msg(key = tweets['data']['created_at'], value = tweets['data']['text'], topic = "INGESTION_TWEETS", producer = get_producer())   

if __name__ == "__main__":
    main()
