import csv

s = "climate change is real nice and dandy, therefore it is great that the greedy politicians are not willing to change climate change, change is not good anyway, climate change"

print(s.count('Climate Change'))

rows = []
with open("GlobalLandTemperaturesByCity.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        print(row[0], row[1])