import json
import re

badData = []

def combineFiles(files):
    data = []
    for file in files:
        with open(file) as file_data:
            data = data + json.load(file_data)
    return data

def cleanData(data):
    # clean it up
    for key, value in data.items():
        if value == "NULL":
            data[key] = ""
    data = cleanupUnits(data)
    # is it bad data? put it somewhere else
    if isVOR(data) or isBadLocation(data):
        return None
    return data

def isBadLocation(data):
    lon = float(data["LongDeg"])
    lat = float(data["LatDeg"])
    if (lat == 0 and lon  == 0) or (lat > 90 or lat < -90) or (lon > 180 or lon < -180):
        data["Bad"] = "Invalid lat/long"
        badData.append(data)
        return True
    return False

def isVOR(data):
    if "VOR" in data["Name"]:
        data["Bad"] = "VOR"
        badData.append(data)
        return True
    return False

def cleanupUnits(data):
    data["Elevation"] = stripUnits(data.pop("Elevation"))
    data["Slope"] = stripUnits(data.pop("Slope"))
    data["RwDirection"] = data.pop("RwDirection")
    data["RwLength"] = stripUnits(data.pop("RwLength"))
    data["RwWidth"] = stripUnits(data.pop("RwWidth"))
    # round to 4 decimal places
    data["LongDeg"] = str(round(float(data["LongDeg"]), 4))
    data["LatDeg"] = str(round(float(data["LatDeg"]), 4))
    return data
    
def stripUnits(data):
    return re.sub("[^0-9]","", data).strip()

def writeToFile(data, filename, indent=False):
    file = open(filename, "w")
    if indent:
        file.write(json.dumps(data, indent=4))
    else:
        file.write(json.dumps(data))
    file.close()

def generateCombinedData(filenames):
    data = combineFiles(filenames)
    data = [cleanData(airstrip) for airstrip in data]
    data = [airstrip for airstrip in data if airstrip]
    writeToFile(badData, "../data/bad_data.json", True)
    writeToFile(data, "../data/combined_maf_data.json")

if __name__ == "__main__":
    #filenames = ['../data/papua_airstrips.json']
    filenames = ['../data/Kalimantan Airstrips.json', '../data/MAF_Served_Airstrips.json', '../data/papua_airstrips.json']
    generateCombinedData(filenames)
