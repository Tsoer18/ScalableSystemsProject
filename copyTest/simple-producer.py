import csv
import threading
import time
from client import get_producer, DEFAULT_TOPIC, produce_msg, send_msg


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def main():
    rows = []
    counter = 0
    measurements = []
    counter2 = 0
    tic = time.perf_counter
    with open("GlobalLandTemperaturesByCity.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            print(row[0], row[1])
            send_msg(key = row[0], value = row[1], topic = "INGESTION", producer = get_producer())
            counter += 1
            if counter == 100 & counter2 < 11:
                toc = time.perf_counter
                measurements.append[tic-toc]
                tic = time.perf_counter
                print("DID ANOTHER MEASUREMENT")
                print(counter2)
                counter = 0
                counter2 += 1
            if counter == 100 & counter2 >= 11:
                print("DONE WITH MEASUREMENTS")
                print(measurements)
                print("_____________________________________________________")
                time.sleep(120)  

if __name__ == "__main__":
    main()
