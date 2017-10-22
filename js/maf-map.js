var map = L.map('map', {
    center: [0, 0],
    zoom: 3
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
//var geojsonLayer = new L.GeoJSON.AJAX("/data/MAF_Served_Airstrips.geojson",
var geojsonLayer = new L.GeoJSON.AJAX("../data/combined_maf_data.geojson", {
    onEachFeature: function popUp(feature, layer) {
        let info = feature.properties;
        let contentTitle = info.DisplayName + "</br>";
        let content = "</br><ul>";
        for(var key in info ){
            content += "<li>"+ key + ":  "+ info[key] + "</li>";
        }
        content += "</ul>";

        if (info.RwLength <  800) {

            contentTitle = feature.properties.Name + " (short runway)";
        }
        layer.bindPopup(contentTitle + content);
    },
    pointToLayer: function(feature, latlng) {
        if (feature.properties.MAFBase === "1") {
            var maf_icon = L.icon({
                iconUrl: "/images/airport.png",
                iconSize:     [20, 20],
                iconAnchor:   [10, 10],
            })
            return L.marker(latlng, {icon: maf_icon});
        }
        if (feature.properties.RwLength < 500) {
            return L.circleMarker(latlng, {
                "color": "#ff0000",
                "fillcolor": "#ff0000",
                "radius": 5,
                "weight": 1,
                "opacity": 1,
                "fillOpacity": 0.8
            });
        }
        else {
            return L.circleMarker(latlng, {
                    "color": "#0000ff",
                    "fillcolor": "#0000ff",
                    "radius": 5,
                    "weight": 1,
                    "opacity": 1,
                    "fillOpacity": 0.8
            });
       }
    }
});
geojsonLayer.addTo(map);
