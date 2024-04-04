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
            <button onclick="updateValue('${feature.id}', 'population')">Update Population Value</button><br>
            Max Capacity: <span id="capacity-${feature.id}">${capacityData[feature.id]?.max_capacity || 'N/A'}</span><br>
            <input type="number" id="new-capacity-${feature.id}" placeholder="Enter new max capacity">
            <button onclick="updateValue('${feature.id}', 'capacity')">Update Max Capacity</button><br>
            Personnel Needed: <span id="personnelNeeded-${feature.id}">${capacityData[feature.id]?.personnel_needed || 'N/A'}</span><br>
            <input type="number" id="new-personnelNeeded-${feature.id}" placeholder="Enter personnel needed">
            <button onclick="updateValue('${feature.id}', 'personnelNeeded')">Update Personnel Needed</button><br>
            Personnel Present: <span id="personnelPresent-${feature.id}">${capacityData[feature.id]?.personnel_present || 'N/A'}</span><br>
            <input type="number" id="new-personnelPresent-${feature.id}" placeholder="Enter personnel present">
            <button onclick="updateValue('${feature.id}', 'personnelPresent')">Update Personnel Present</button><br>
            Transport Methods: <span id="transport-${feature.id}">${capacityData[feature.id]?.transport || 'N/A'}</span><br>
            <input type="number" id="new-transport-${feature.id}" placeholder="Enter new transport">
            <button onclick="updateValue('${feature.id}', 'transport')">Update Transport Method</button>
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
            <button onclick="updateValue('${feature.id}', 'population')">Update Population Value</button><br>
            Max Capacity: <span id="capacity-${feature.id}">${capacityData[feature.id]?.max_capacity || 'N/A'}</span><br>
            <input type="number" id="new-capacity-${feature.id}" placeholder="Enter new max capacity">
            <button onclick="updateValue('${feature.id}', 'capacity')">Update Max Capacity</button><br>
            Personnel Needed: <span id="personnelNeeded-${feature.id}">${capacityData[feature.id]?.personnel_needed || 'N/A'}</span><br>
            <input type="number" id="new-personnelNeeded-${feature.id}" placeholder="Enter personnel needed">
            <button onclick="updateValue('${feature.id}', 'personnelNeeded')">Update Personnel Needed</button><br>
            Personnel Present: <span id="personnelPresent-${feature.id}">${capacityData[feature.id]?.personnel_present || 'N/A'}</span><br>
            <input type="number" id="new-personnelPresent-${feature.id}" placeholder="Enter personnel present">
            <button onclick="updateValue('${feature.id}', 'personnelPresent')">Update Personnel Present</button><br>
            Transport Methods: <span id="transport-${feature.id}">${capacityData[feature.id]?.transport || 'N/A'}</span><br>
            <input type="number" id="new-transport-${feature.id}" placeholder="Enter new transport">
            <button onclick="updateValue('${feature.id}', 'transport')">
            Update Transport Method</button>
            `;
        return L.marker(latlng).bindPopup(popupContent);
    }
}

// Function to update the values
function updateValue(stationId, type) {
    console.log(type, stationId)
    const newValue = document.getElementById(`new-${type}-${stationId}`).value;

    // Proceed only if newValue is not empty
    if (newValue) {
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
                // Update the displayed label based on type
                if (type === 'population') {
                    capacityData[stationId].current_population = newValue;
                    document.getElementById(`population-${stationId}`).textContent = newValue;
                } else if (type === 'capacity') {
                    capacityData[stationId].max_capacity = newValue;
                    document.getElementById(`capacity-${stationId}`).textContent = newValue;
                } else if (type === 'personnelNeeded') {
                    capacityData[stationId].personnel_needed = newValue;
                    document.getElementById(`personnelNeeded-${stationId}`).textContent = newValue;
                } else if (type === 'personnelPresent') {
                    capacityData[stationId].personnel_present = newValue;
                    document.getElementById(`personnelPresent-${stationId}`).textContent = newValue;
                } else if (type === 'transport') {
                    capacityData[stationId].transport = newValue;
                    document.getElementById(`transport-${stationId}`).textContent = newValue;
                }
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

                // Connect nodes based on their connections
                connectNodes(nodes);
            })
            .catch(error => console.error('Error loading GeoJSON:', error));
    })
    .catch(error => console.error('Error fetching capacities:', error));

// Function to connect nodes based on their connections
function connectNodes(nodes) {
    for (const nodeId in nodes) {
        const node = nodes[nodeId];
        const { x: x1, y: y1 } = node;
        const latLng1 = L.latLng(y1, x1);

        for (const connectedNodeId of node.connections) {
            const connectedNode = nodes[connectedNodeId];
            const { x: x2, y: y2 } = connectedNode;
            const latLng2 = L.latLng(y2, x2);

            L.polyline([latLng1, latLng2], { color: 'blue' }).addTo(map);
        }
    }
}


var evacuationTime = 50; // Initial evacuation time in minutes, adjust as needed
