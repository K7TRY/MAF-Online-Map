/*
 * Data schema
 * {
 *  "Program": "EC",
 *  "AirstripID": "AS000001",
 *  "DisplayName": "SHL",
 *  "Name": "Shell",
 *  "ICAO": "SESM",
 *  "GPS": "NULL",
 *  "LatDeg": "-1.50472223758698",
 *  "LongDeg": "-78.0633316040039",
 *  "Variation": "NULL",
 *  "Elevation": "3415",
 *  "RwDirection": "12-20",
 *  "RwClass": "1",
 *  "RwSurface": "Paved",
 *  "RwLength": "1500",
 *  "TODA": "NULL",
 *  "RwWidth": "25",
 *  "Wet": "NULL",
 *  "Dry": "NULL",
 *  "Slope": "NULL",
 *  "MAFBase": "1"
 * }
 */

$.get("data/combined_maf_data.json", function (data) {
    const airstrip_data = data;

    const program_to_country = {
        EDRC: 'CG',
        WDRC: 'CD',
        HT: 'HT',
        LS: 'LS',
        MOZ: 'MZ',
        NAM: 'US',
        ID: 'ID',
    };
    //map  json country codes to map country codes

    const in_countries = airstrip_data.reduce((values, airstrip) => {
        values[program_to_country[airstrip.Program]] = 1;
        return values;
    }, {});
    //marker data needed
    const marker_data = airstrip_data.map((airstrip) => {
        return {
            latLng: [airstrip.LatDeg, airstrip.LongDeg],
            name: airstrip.Name,
            status: airstrip.MAFBase,
        };
    });
    $('#map').vectorMap({
        map: 'world_mill',
        markers: marker_data,
        series: {
            regions: [{
                hoverOpacity: 0.7,
                hoverColor: false,
                values: in_countries,
                scale: ['#FFFFFF', '#0071A4'],
                normalizeFunction: 'polynomial',
            }],
            markers: [
                marker_data,
                {
                    attribute: 'image',
                    scale: {
                        'FLY': 'images/airport.png',
                    },
                    values: airstrip_data.reduce((values, airstrip, index) => {
                        if (airstrip.MAFBase === "1") {
                            values[index] = "FLY";
                        }
                        return values;
                    }, {}),
                    legend: {
                        horizontal: true,
                        title: 'MAF bases and destinations',
                        labelRender: (v) => {
                            return {
                                FLY: 'MAF Base',
                            }[v];
                        }
                    }
                }
            ],
            onRegionClick: function () {

            }
        },
        backgroundColor: '#383f47'
    });
});