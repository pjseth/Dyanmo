// Initialize the map
var map = L.map('map').setView([37.5665, 126.9780], 10);

// Load and display OSM tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Function to get the English name of a feature
function getEnglishName(properties) {
    return properties['name:en'] || properties['name'];
}

// Function to handle rail lines
function handleRailLines(feature, layer) {
    if (feature.properties) {
        let popupContent = `<strong>${getEnglishName(feature.properties)}</strong><br>` +
                           `Current Population: ${feature.properties.current_pop}<br>` +
                           `Max Capacity: ${feature.properties.max_capacity}`;
        layer.bindPopup(popupContent);
    }
}

// Function to handle stations
function handleStations(feature, latlng) {
    if (feature.properties) {
        let popupContent = `<strong>${getEnglishName(feature.properties)}</strong><br>` +
                           `Current Population: ${feature.properties.current_pop}<br>` +
                           `Max Capacity: ${feature.properties.max_capacity}`;
        return L.marker(latlng).bindPopup(popupContent);
    }
}

// Load the GeoJSON file
fetch('rail_network.geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            onEachFeature: handleRailLines,
            pointToLayer: handleStations
        }).addTo(map);
    })
    .catch(error => console.error('Error loading GeoJSON:', error));