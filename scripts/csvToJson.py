import csv
import json

def csvToJson(file):
    out = []
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(row)
    return out

def writeToFile(data, filename):
    file = open(filename, "w")
    file.write(json.dumps(data))
    file.close()

def generateFromCsv(filenames):
    for filename in filenames:
        data = csvToJson(filename + ".csv")
        writeToFile(data, filename + ".json")

if __name__ == "__main__":
    filenames = ['../data/MAF_Served_Airstrips']
    generateFromCsv(filenames)
