import json
import re

def combineFiles(files):
    data = []
    for file in files:
        with open(file) as file_data:
            data = data + json.load(file_data)
    return data

def cleanData(data):
    for key, value in data.items():
        if value == "NULL":
            data[key] = ""
    # more cleaning needs done? put it here
    data["Elevation"] = stripUnits(data.pop("Elevation"))
    data["Slope"] = stripUnits(data.pop("Slope"))
    data["RwDirection"] = data.pop("RwDirection")
    data["RwLength"] = stripUnits(data.pop("RwLength"))
    data["RwWidth"] = stripUnits(data.pop("RwWidth"))
    return data

def stripUnits(data):
    return re.sub("[^0-9]","", data).strip()

def writeToFile(data, filename):
    file = open(filename, "w")
    file.write(json.dumps(data))
    file.close()

def generateCombinedData(filenames):
    data = combineFiles(filenames)
    data = [cleanData(airstrip) for airstrip in data]
    writeToFile(data, "../data/combined_maf_data.json")

if __name__ == "__main__":
    #filenames = ['../data/papua_airstrips.json']
    filenames = ['../data/Kalimantan Airstrips.json', '../data/MAF_Served_Airstrips.json', '../data/papua_airstrips.json']
    generateCombinedData(filenames)



#TODO filter out VORs
#TODO filter out lat/long 0,0
