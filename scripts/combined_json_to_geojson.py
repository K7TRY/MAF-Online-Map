import json

INPUT_JSON = "../data/combined_maf_data.json"
OUTPUT_GEOJSON = "../data/combined_maf_data.geojson"


def main():
    with open(INPUT_JSON) as f:
        airports_json = json.load(f)

    airports_geojson = []

    for airport in airports_json:
        # Int-ify runway length
        try:
            airport["RwLength"] = int(airport["RwLength"])
        except ValueError:
            airport["RwLength"] = ""
        gja = {}
        gja["type"] = "Feature"
        gja["properties"] = airport
        gja["geometry"] = {
            "type": "Point",
            "coordinates": [airport["LongDeg"], airport["LatDeg"]],
        }
        airports_geojson.append(gja)

    with open(OUTPUT_GEOJSON, "w") as f:
        json.dump(airports_geojson, f)


if __name__ == "__main__":
    main()
