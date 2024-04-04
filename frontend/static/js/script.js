// Initialize the map
var map = L.map('map').setView([37.5665, 126.9780], 16);

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



// Function to handle stations
function handleStations(feature, latlng) {
    if (feature.properties) {
        let markerColor;
        switch (feature.properties.color) {
            case 1:
                markerColor = '#FF0000'; // Red for 's'
                break;
            case 2:
                markerColor = '#000000'; // Black for 'i'
                break;
            case 3:
                markerColor = '#0000FF'; // Blue for 'd'
                break;
            default:
                markerColor = '#000000'; // Default to black
        }
        
        let popupContent = `
            <strong>${getEnglishName(feature.properties)}</strong><br>
            Total Evacuation Vehicle Number: <span id="vehicle-${feature.id}">${capacityData[feature.id]?.current_population || 'N/A'}</span><br>
            <input type="number" id="vehicle-number-${feature.id}" placeholder="Enter Number">
            <button onclick="updateValue('${feature.id}', 'vehicle')">Update Vehicle Number</button><br>
            `;

        return L.circleMarker(latlng, { color: markerColor }).bindPopup(popupContent);
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
                    document
                    .getElementById(`transport-${stationId}`).textContent = newValue;
                }
            })
            .catch((error) => {
                console.error(`Error updating ${type}:`, error);
            });
    } else {
        alert(`Please enter a new ${type} value.`);
    }
}

// Define the nodes with coordinates and connections
const nodes = {
    0: { x: 126.9731, y: 37.5664, color: 1, connections: [1, 2] },
    1: { x: 126.9706, y: 37.5654, color: 2, connections: [0, 4, 9] },
    2: { x: 126.9753, y: 37.5656, color: 2, connections: [0, 3, 7, 11] },
    3: { x: 126.9774, y: 37.5664, color: 2, connections: [2, 17, 19] },
    4: { x: 126.9691, y: 37.5651, color: 2, connections: [1, 5, 16] },
    5: { x: 126.9691, y: 37.5641, color: 2, connections: [4, 18] },
    6: { x: 126.9729, y: 37.5641, color: 2, connections: [0, 7, 18] },
    7: { x: 126.9756, y: 37.5641, color: 2, connections: [2, 6, 19] },
    8: { x: 126.9675, y: 37.5665, color: 2, connections: [9, 14, 16] },
    9: { x: 126.9704, y: 37.5671, color: 2, connections: [1, 8, 10, 13] },
    10: { x: 126.9756, y: 37.5671, color: 2, connections: [9, 11, 12] },
    11: { x: 126.9774, y: 37.5676, color: 2, connections: [2, 10, 15] },
    12: { x: 126.9755, y: 37.5681, color: 2, connections: [10, 13, 15] },
    13: { x: 126.9706, y: 37.5686, color: 3, connections: [9, 12] },
    14: { x: 126.9691, y: 37.5682, color: 3, connections: [8] },
    15: { x: 126.9774, y: 37.5687, color: 3, connections: [11, 12] },
    16: { x: 126.9676, y: 37.5681, color: 3, connections: [4, 8, 14] },
    17: { x: 126.9774, y: 37.5664, color: 3, connections: [3] },
    18: { x: 126.9676, y: 37.5641, color: 3, connections: [5, 6] },
    19: { x: 126.9774, y: 37.5641, color: 3, connections: [3, 7] },
};

// Initialize the GeoJSON object
const geojson = {
    "type": "FeatureCollection",
    "features": []
};

// Define marker colors for each type
const markerColors = {
    's': '#000000', // Black for 's'
    'i': '#FF0000', // Red for 'i'
    'd': '#0000FF'  // Blue for 'd'
};

// Add features for each node
for (const nodeId in nodes) {
    const node = nodes[nodeId];
    const feature = {
        "type": "Feature",
        "properties": {
            "type": "node",
            "name": nodeId,
            "color": node.color
        },
        "geometry": {
            "type": "Point",
            "coordinates": [node.x, node.y]
        }
    };
    geojson.features.push(feature);
}

// Add connecting lines
for (const nodeId in nodes) {
    const node = nodes[nodeId];
    for (const connectedNodeId of node.connections) {
        const line = {
            "type": "Feature",
            "properties": {
                "type": "line",
                "name": "connect"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [node.x, node.y],
                    [nodes[connectedNodeId].x, nodes[connectedNodeId].y]
                ]
            }
        };
        geojson.features.push(line);
    }
}

// Use the generated GeoJSON object directly
L.geoJSON(geojson, {
    pointToLayer: handleStations
}).addTo(map);

// Initialize evacuation time
var evacuationTime = 50; // Initial evacuation time in minutes, adjust as needed

// Define multiple paths
var paths = [
    [0, 6, 18],
    [0, 1, 9, 8, 16],
    [0, 1, 9, 13],
    [0, 2, 3, 17],
    [0, 2, 3, 19]
];

// Array to hold animated markers for each path
var animatedMarkers = [];

// Function to animate a marker along a path
function animateMarker(marker, path) {
    var index = 0; // Start from the source node
    var length = path.length;
    var duration = 4000; // Duration of animation in milliseconds
    var startTime; // Variable to store the start time of the animation

    function moveMarker() {
        if (index < length - 1) {
            var node = nodes[path[index]];
            var nextNode = nodes[path[index + 1]];
            if (nextNode) {
                if (!startTime) {
                    startTime = new Date().getTime();
                }
                var currentTime = new Date().getTime();
                var elapsedTime = currentTime - startTime;
                var fraction = elapsedTime / duration;
                if (fraction < 1) {
                    var interpolatedLatLng = L.latLng(
                        node.y + fraction * (nextNode.y - node.y),
                        node.x + fraction * (nextNode.x - node.x)
                    );
                    marker.setLatLng(interpolatedLatLng);
                } else {
                    index++;
                    startTime = null;
                }
            } else {
                clearInterval(marker.interval);
            }
        } else {
            clearInterval(marker.interval);
        }
    }

    marker.interval = setInterval(moveMarker, 20); // Interval for smoother animation
}



// Function to create and animate markers for each path
function animatePaths() {
    paths.forEach(function(path) {
        var marker = L.circleMarker([nodes[path[0]].y, nodes[path[0]].x], { color: 'red', fillColor: 'red', fillOpacity: 1, radius: 5 }).addTo(map);
        animatedMarkers.push(marker);
        animateMarker(marker, path);
    });
}

// Call the function to start animating paths
animatePaths();

