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

// Global object to hold capacity data
var capacityData = {};

// Function to handle rail lines
function handleRailLines(feature, layer) {
    if (feature.properties) {
        let popupContent = `
            <strong>${getEnglishName(feature.properties)}</strong><br>
            Current Population: <span id="population-${feature.id}">${capacityData[feature.id]?.current_population || 'N/A'}</span><br>
            <input type="number" id="new-population-${feature.id}" placeholder="Enter new population">
            <button onclick="updateValue('${feature.id}', 'population')">Update Population</button><br>
            Max Capacity: <span id="capacity-${feature.id}">${capacityData[feature.id]?.max_capacity || 'N/A'}</span><br>
            <input type="number" id="new-capacity-${feature.id}" placeholder="Enter new max capacity">
            <button onclick="updateValue('${feature.id}', 'capacity')">Update Max Capacity</button>
        `;
        layer.bindPopup(popupContent);
    }
}

// Function to handle stations
function handleStations(feature, latlng) {
    if (feature.properties) {
        let popupContent = `
            <strong>${getEnglishName(feature.properties)}</strong><br>
            Current Population: <span id="population-${feature.id}">${capacityData[feature.id]?.current_population || 'N/A'}</span><br>
            <input type="number" id="new-population-${feature.id}" placeholder="Enter new population">
            <button onclick="updateValue('${feature.id}', 'population')">Update Population</button><br>
            Max Capacity: <span id="capacity-${feature.id}">${capacityData[feature.id]?.max_capacity || 'N/A'}</span><br>
            <input type="number" id="new-capacity-${feature.id}" placeholder="Enter new max capacity">
            <button onclick="updateValue('${feature.id}', 'capacoty')">Update Max Capacity</button>
        `;
        return L.marker(latlng).bindPopup(popupContent);
    }
}

// Function to update the population
function updateValue(stationId, type) {
    const newValue = document.getElementById(`new-${type}-${stationId}`).value;

    // Proceed only if newValue is not empty
    if(newValue) {
        fetch(`/api/update${type.charAt(0).toUpperCase() + type.slice(1)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: stationId, newValue: newValue })
        })
        .then(response => response.json())
        .then(data => {
            console.log(`${type.charAt(0).toUpperCase() + type.slice(1)} updated:`, data);
            capacityData[stationId][`current_${type}`] = newValue;
            // Update the displayed label
            document.getElementById(`${type === 'population' ? 'population' : 'capacity'}-${stationId}`).textContent = newValue;
        })
        .catch((error) => {
            console.error(`Error updating ${type}:`, error);
        });
    } else {
        alert(`Please enter a new ${type} value.`);
    }
}

// Fetch capacities from the backend API
fetch('/api/capacities')
    .then(response => response.json())
    .then(data => {
        // Store capacity data
        capacityData = data;

        // Then load the GeoJSON data
        fetch('/rail_network.geojson')
            .then(response => response.json())
            .then(data => {
                L.geoJSON(data, {
                    onEachFeature: handleRailLines,
                    pointToLayer: handleStations
                }).addTo(map);
            })
            .catch(error => console.error('Error loading GeoJSON:', error));
    })
    .catch(error => console.error('Error fetching capacities:', error));
