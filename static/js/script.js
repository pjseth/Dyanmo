// PJ's Code
// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.getElementById('evacuation-form');
//     const resultDiv = document.getElementById('result');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const address = document.getElementById('address').value;

//         fetch('/calculate_evacuation', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ address: address })
//         })
//         .then(response => response.json())
//         .then(data => {
//             resultDiv.innerHTML = `Evacuation Capacity: ${data.evacuation_capacity}`;
//         })
//         .catch(error => {
//             resultDiv.innerHTML = 'Error calculating evacuation capacity.';
//         });
//     });
// });

// Initialize the map
var map = L.map('map').setView([37.5665, 126.9780], 13); // Centered on Seoul as an example

// Load and display OSM tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var graph = new Graph();

// Example nodes and display
graph.addFixedNode("Location1", 37.5622, 126.9784, 100, false, 50);
graph.addTransportNode("Transport1", 37.5700, 126.9800, 200, 100, true);

for (let nodeName in graph.fixed_nodes) {
    let node = graph.fixed_nodes[nodeName];
    L.marker([node.lat, node.lon]).addTo(map).bindPopup(nodeName + "<br>Population: " + node.current_population);
}

for (let nodeName in graph.transport_nodes) {
    let node = graph.transport_nodes[nodeName];
    L.marker([node.lat, node.lon]).addTo(map).bindPopup(nodeName + "<br>Capacity: " + node.evacuation_capacity);
}