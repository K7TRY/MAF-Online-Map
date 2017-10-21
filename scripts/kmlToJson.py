import json
import xml.etree.ElementTree

emptyPlacemark = {
        "Program": None,
        "AirstripID": None,
        "DisplayName": None,
        "Name": None,
        "ICAO": None,
        "GPS": None,
        "LatDeg": None,
        "LongDeg": None,
        "Variation": None,
        "Elevation": None,
        "RwDirection": None,
        "RwClass": None,
        "RwSurface": None,
        "RwLength": None,
        "TODA": None,
        "RwWidth": None,
        "Wet": None,
        "Dry": None,
        "Slope": None,
        "MAFBase": None
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

def kmlToJson(file):
    out = []
    root = xml.etree.ElementTree.parse(file).getroot()
    placemarkers = root.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    print("found", len(placemarkers), "placemarkers")

    for placemarker in placemarkers:
        out.append(placemarkerToJson(placemarker))
    return json.dumps(out)

def placemarkerToJson(placemarker):
    out = emptyPlacemark
    out["DisplayName"] = placemarker.find("{http://www.opengis.net/kml/2.2}name").text
    coords = placemarker.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
    out["LongDeg"] = coords.split(",")[0]
    out["LatDeg"] = coords.split(",")[1]
    out["Description"] = placemarker.find(".//{http://www.opengis.net/kml/2.2}description").text
    #Name: Yogesem\nElev: 7600'\nSlope: 10%\nApproach Rwy: 27/--\nLength: 479 m\nWidth: 28 m"
    out = dict(out.items() + processDescription(out).items())
    return out

def processDescription(data):
    # check description
    description = {}
    desc = data["Description"]
    descChunks = len(desc.split("\n"))
    if(descChunks < 2)
        return description
    # TODO more processing here to break out papua data
    return description

def writeToFile(data, filename):
    file = open(filename, "w")
    file.write(data)
    file.close()

if __name__ == "__main__":
    filename = '../Kalimantan Airstrips'
    #filename = '../papua_airstrips'
    data = kmlToJson(filename + ".kml")
    writeToFile(data, filename + ".json")
