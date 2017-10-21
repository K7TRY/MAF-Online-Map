import copy
import json
import re
import xml.etree.ElementTree

emptyPlacemark = {
        "Program": "",
        "AirstripID": "",
        "DisplayName": "",
        "Name": "",
        "ICAO": "",
        "GPS": "",
        "LatDeg": "",
        "LongDeg": "",
        "Variation": "",
        "Elevation": "",
        "RwDirection": "",
        "RwClass": "",
        "RwSurface": "",
        "RwLength": "",
        "TODA": "",
        "RwWidth": "",
        "Wet": "",
        "Dry": "",
        "Slope": "",
        "MAFBase": ""
    }
examplePlacemark = {
        "Program": "EC",
        "AirstripID": "AS000002",
        "DisplayName": "MNT",
        "Name": "Montalvo",
        "ICAO": "SEMO",
        "GPS": "NULL",
        "LatDeg": "-2.06716656684875",
        "LongDeg": "-76.9761657714844",
        "Variation": "NULL",
        "Elevation": "1000",
        "RwDirection": "08/26",
        "RwClass": "1",
        "RwSurface": "asphalt",
        "RwLength": "1480",
        "TODA": "NULL",
        "RwWidth": "24",
        "Wet": "NULL",
        "Dry": "NULL",
        "Slope": "0",
        "MAFBase": "0"
    }

def kmlToJson(file, defaultPlacemark):
    out = []
    root = xml.etree.ElementTree.parse(file).getroot()
    placemarkers = root.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    print("found", len(placemarkers), "placemarkers")

    for placemarker in placemarkers:
        out.append(placemarkerToJson(placemarker, defaultPlacemark))
    return out

def placemarkerToJson(placemarker, defaultPlacemark):
    out = copy.copy(defaultPlacemark)
    out["DisplayName"] = placemarker.find("{http://www.opengis.net/kml/2.2}name").text
    coords = placemarker.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
    out["LongDeg"] = coords.split(",")[0]
    out["LatDeg"] = coords.split(",")[1]
    out["Description"] = placemarker.find(".//{http://www.opengis.net/kml/2.2}description").text
    out.update(processDescription(out))
    out.pop("Description")
    return out

def processDescription(data):
    # check description
    description = {}
    desc = data["Description"]
    descChunks = desc.split("\n")
    if(len(descChunks) < 2):
        return description
    # more processing here to break out papua data
    description = dict((chunk.split(":")) for chunk in descChunks)
    description["Elevation"] = stripUnits(description.pop("Elev"))
    description["Slope"] = stripUnits(description.pop("Slope"))
    description["RwDirection"] = description.pop("Approach Rwy")
    description["RwLength"] = stripUnits(description.pop("Length"))
    description["RwWidth"] = stripUnits(description.pop("Width"))
    return description

def stripUnits(data):
    return re.sub("[^0-9]","", data).strip()

def writeToFile(data, filename):
    file = open(filename, "w")
    file.write(json.dumps(data))
    file.close()

def indonesiaPlacemark():
    indonesiaPlacemark = emptyPlacemark
    indonesiaPlacemark.update({"Program": "ID"})
    return indonesiaPlacemark

def generateFromKml(filenames):
    defaultPlacemark = indonesiaPlacemark()
    for filename in filenames:
        data = kmlToJson(filename + ".kml", defaultPlacemark)
        writeToFile(data, filename + ".json")

if __name__ == "__main__":
    filenames = ['../data/Kalimantan Airstrips', '../data/papua_airstrips']
    generateFromKml(filenames)
