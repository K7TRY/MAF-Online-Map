import csv
import json

def csvToJson(file):
    out = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(row)
    return json.dumps(out)

def writeToFile(data, filename):
    file = open(filename, "w")
    file.write(data)
    file.close()

if __name__ == "__main__":
    filename = '../data/MAF_Served_Airstrips'
    data = csvToJson(filename + ".csv")
    writeToFile(data, filename + ".json")
