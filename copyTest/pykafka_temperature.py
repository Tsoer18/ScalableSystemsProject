from client import get_consumer, DEFAULT_TOPIC, recive_msg, DEFAULT_CONSUMER, receive_msg_temperature
import sys


def main():
    args = sys.argv[1:]
    group_id = args[0] if len(args) == 1 else DEFAULT_CONSUMER

    print(f"group_id={group_id}")
    consumer = get_consumer(topic = "INGESTION", group_id=group_id)

    try:
        receive_msg_temperature(consumer)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
