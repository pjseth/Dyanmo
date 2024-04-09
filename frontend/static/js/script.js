// Initialize the map
var map = L.map('map').setView([37.5759, 126.9768], 15);

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
        let popupContent;
        let interactive = true; // Determine if the marker is interactive
        switch (feature.properties.color) {
            case 1:
                console.log("here color")
                console.log(nodes[feature.properties.name].name)
                markerColor = '#FF0000'; // Red
                popupContent = `
                    <strong>${nodes[feature.properties.name].name}</strong><br>
                    Total Evacuation Vehicle Number: <span id="vehicle-${feature.id}">${capacityData[feature.id]?.current_population || 'N/A'}</span><br>
                    <input type="number" id="node-${nodes[feature.properties.name].name}-evac-num" placeholder="Enter Number">
                    <button onclick="updateValue('${nodes[feature.properties.name].name}')">Update Vehicle Number</button><br>
                    Batch Interval: <span id="capacity-${feature.id}">${capacityData[feature.id]?.max_capacity || 'N/A'}</span><br>
                    <input type="number" id="new-capacity-${feature.id}" placeholder="Enter Number">
                    <button onclick="updateValue('${feature.id}', 'capacity')">Update Batch Interval</button><br>
                `;
                break;
            case 2:
                markerColor = '#000000'; //Black
                popupContent = nodes[feature.properties.name].name; // Set popup content to node name
                interactive = false; // Make marker interactive for non-source nodes
                break;
            case 3:
                markerColor = '#0000FF'; //Blue
                popupContent = nodes[feature.properties.name].name; // Set popup content to node name
                interactive = false; // Make marker interactive for non-source nodes
                break;
            default:
                markerColor = '#000000'; // Default to black
                popupContent = nodes[feature.properties.name].name; // Set popup content to node name
                interactive = false; // Make marker interactive for non-source nodes
        }

        // Create custom marker icon with label
        const customIcon = L.divIcon({
            className: 'custom-icon',
            html: `<div class="marker-label" style="color: ${markerColor}">${nodes[feature.properties.name].name}</div>`,
            iconSize: [80, 30],
            iconAnchor: [40, 15]
        });
        
        // Create marker with custom icon
        const marker = L.marker(latlng, { icon: customIcon });

        // Add popup
        marker.bindPopup(popupContent);
        if (interactive) {
//             marker.on('mouseover', function (e) {
//                 this.openPopup();
//             });
//             marker.on('mouseout', function (e) {
//                 this.closePopup();
//             });
            // Add event listeners for hover inside the circle
            marker.on('click', function (e) {
                this.openPopup();
            });
//             marker.on('mouseout', function (e) {
//                 this.closePopup();
//             });

        }
        // Set marker interactivity
        // if (interactive) {
        //     marker.on('click', function (e) {
        //         // Call updateValue function when label is clicked
        //         updateValue(nodes[feature.properties.name].name);
        //     });
        // }
        return marker;
    }
}

// Add CSS for marker label styling
var markerLabelStyle = document.createElement('style');
markerLabelStyle.type = 'text/css';
markerLabelStyle.innerHTML = `
    .marker-label {
        background-color: white;
        border: 1px solid #000;
        border-radius: 5px;
        padding: 3px;
        font-weight: bold;
        font-size: 10px;
        text-align: center;
        cursor: pointer;
    }
`;
document.head.appendChild(markerLabelStyle);

// Function to update the values
function updateValue(node) {
    console.log(node);

    // Proceed only if newValue is not empty
    if (node) {
        totalEvacuationFlow = Number(document.getElementById(`node-${node}-evac-num`).value);
        console.log("got here", totalEvacuationFlow);
        initiateEvacuation(totalEvacuationFlow);
    } else {
        alert(`Please enter a new ${type} value.`);
    }
}

// Add event listener for when the page is fully loaded
window.addEventListener('load', function() {
    // Open a popup with instructions when the page is loaded
    var popup = L.popup()
        .setLatLng([37.5759, 126.9768]) // Set coordinates for the popup
        .setContent("Click the source node and input total evacuation time.") // Set content for the popup
        .openOn(map); // Open the popup on the map

    // Add event listener to close the popup when clicked
    map.on('click', function() {
        map.closePopup(popup);
    });
});

// Function to initiate the evacuation process
function initiateEvacuation(totalEvacuationFlow) {
    console.log("here", totalEvacuationFlow);
    fetch('/api/evacuation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ total_evacuation_flow: totalEvacuationFlow })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Evacuation result:', data);
        // Update paths array with unique routes taken
        paths = data.unique_routes_taken;
        // Update evacuation time with total time
        evacuation_time = data.total_time.toFixed(2);
        document.getElementById('evacuation-time').textContent = `${evacuation_time} minutes`; 
        // Call function to update markers on the map or perform any other actions
        updateMarkersOnMap();
    })
    .catch(error => {
        console.error('Error initiating evacuation:', error);
    });
}

// Function to update markers on the map
function updateMarkersOnMap() {
    // Remove existing animated markers
    animatedMarkers.forEach(function(marker) {
        marker.remove();
    });

    // Call the function to start animating paths
    animatePaths();
}

// Define the nodes with coordinates and connections
const nodes = {
    0: { name: "Gwanghwamun Square", x: 126.9768, y: 37.5759, color: 1, connections: [1, 2] },
    1: { name: "Sejong Center for the Performing Arts", x: 126.9738, y: 37.5749, color: 2, connections: [0, 4, 9] },
    2: { name: "Kyobo Book Centre (Main Store)", x: 126.9798, y: 37.5769, color: 2, connections: [0, 3, 7, 11] },
    3: { name: "Jogyesa Temple", x: 126.9828, y: 37.5759, color: 2, connections: [2, 17, 19] },
    4: { name: "Seoul Museum of History", x: 126.9718, y: 37.5739, color: 2, connections: [1, 5, 16] },
    5: { name: "Jeongdok Public Library", x: 126.9718, y: 37.5719, color: 2, connections: [4, 18] },
    6: { name: "Cheonggyecheon Stream (near Gwanggyo Bridge)", x: 126.9748, y: 37.5719, color: 2, connections: [0, 7, 18] },
    7: { name: "Bosingak Belfry", x: 126.9798, y: 37.5719, color: 2, connections: [2, 6, 19] },
    8: { name: "Gyeonghuigung Palace", x: 126.9698, y: 37.5759, color: 2, connections: [9, 14, 16] },
    9: { name: "Sajik Park", x: 126.9728, y: 37.5789, color: 2, connections: [1, 8, 10, 13] },
    10: { name: "Jongmyo Shrine", x: 126.9798, y: 37.5789, color: 2, connections: [9, 11, 12] },
    11: { name: "Changdeokgung Palace", x: 126.9828, y: 37.5799, color: 2, connections: [2, 10, 15] },
    12: { name: "Changgyeonggung Palace", x: 126.9798, y: 37.5809, color: 2, connections: [10, 13, 15] },
    13: { name: "Sungkyunkwan University (Main Campus)", x: 126.9728, y: 37.5819, color: 3, connections: [9, 12] },
    14: { name: "Inwangsan Mountain (Southern trails)", x: 126.9698, y: 37.5819, color: 3, connections: [8] },
    15: { name: "Naksan Park", x: 126.9828, y: 37.5829, color: 3, connections: [11, 12] },
    16: { name: "Seoul Science Park", x: 126.9698, y: 37.5809, color: 3, connections: [4, 8, 14] },
    17: { name: "Unhyeongung Royal Residence", x: 126.9828, y: 37.5759, color: 3, connections: [3] },
    18: { name: "Marronnier Park", x: 126.9698, y: 37.5719, color: 3, connections: [5, 6] },
    19: { name: "Dongdaemun Design Plaza (DDP)", x: 126.9828, y: 37.5719, color: 3, connections: [3, 7] },
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
    'd': '#0000FF'  // Blue for 'd'
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
const geojsonLayer = L.geoJSON(geojson, {
    pointToLayer: handleStations
}).addTo(map);

// Add event listener to marker labels
geojsonLayer.eachLayer(function (layer) {
    if (layer instanceof L.Marker) {
        const markerLabel = layer.getElement().querySelector('.marker-label');
        if (markerLabel) {
            markerLabel.addEventListener('click', function () {
                layer.openPopup();
                const feature = layer.feature;
                if (feature.properties && feature.properties.color === 2 || feature.properties.color === 3) {
                    updateValue(nodes[feature.properties.name].name);
                }
            });
        }
    }
});

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

// Add CSS for animated markers to display on top
var animatedMarkerStyle = document.createElement('style');
animatedMarkerStyle.type = 'text/css';
animatedMarkerStyle.innerHTML = `
    .animated-marker {
        z-index: 4000; /* Set a high z-index value to ensure it appears above other elements */
    }
`;
document.head.appendChild(animatedMarkerStyle);


// Function to create and animate markers for each path
function animatePaths() {
    paths.forEach(function(path) {
        var marker = L.circleMarker([nodes[path[0]].y, nodes[path[0]].x], { 
            color: 'red', 
            fillColor: 'red', 
            fillOpacity: 2, 
            radius: 5,
            className: 'animated-marker' // Add class to apply style
        }).addTo(map);
        animatedMarkers.push(marker);
        animateMarker(marker, path);
    });
}

// Call the function to start animating paths
//animatePaths();