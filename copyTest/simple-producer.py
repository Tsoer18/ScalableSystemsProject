import threading
from client import get_producer, DEFAULT_TOPIC, produce_msg, send_msg


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def main():
    rows = []
    with open("GlobalLandTemperaturesByCity.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        print(row[0], row[1])
        send_msg(key = row[0], value = row[1], topic = "INGESTION")   

if __name__ == "__main__":
    main()
