var geojsonMarkerOptions = {
	    radius: 8,
	    fillColor: "#ff7800",
	    color: "#000",
	    weight: 1,
	    opacity: 1,
	    fillOpacity: 0.8
};

function popUp(feature, layer) {
	layer.bindPopup(feature.properties.Name);
}

var map = L.map('map', {
	center: [0, -78],
	zoom: 5
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
var geojsonLayer = new L.GeoJSON.AJAX("/data/MAF_Served_Airstrips.geojson",
	{onEachFeature:popUp}
);  
geojsonLayer.addTo(map)
