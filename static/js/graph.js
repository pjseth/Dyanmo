class Node {
    constructor(lat, lon, evacuation_capacity=0, sea_node=false, current_population=0) {
        this.lat = lat;
        this.lon = lon;
        this.evacuation_capacity = evacuation_capacity;
        this.current_population = current_population;
        this.sea_node = sea_node;
    }

    isEvacuationPoint() {
        return this.evacuation_capacity > 0;
    }
}

class Connection {
    constructor(nodeA, nodeB, capacity, time) {
        this.nodeA = nodeA;
        this.nodeB = nodeB;
        this.capacity = capacity;
        this.time = time;
    }

    getDistance() {
        let dLat = this.nodeA.lat - this.nodeB.lat;
        let dLon = this.nodeA.lon - this.nodeB.lon;
        return Math.sqrt(dLat * dLat + dLon * dLon);
    }
}

class Graph {
    constructor() {
        this.fixed_nodes = {};
        this.transport_nodes = {};
        this.connections = [];
    }

    addFixedNode(name, lat, lon, evacuation_capacity=0, sea_node=false, current_population=0) {
        this.fixed_nodes[name] = new Node(lat, lon, evacuation_capacity, sea_node, current_population);
    }

    addTransportNode(name, lat, lon, evacuation_capacity, dist_until_refuel, sea_node=false) {
        let transportNode = new Node(lat, lon, evacuation_capacity, sea_node);
        transportNode.dist_until_refuel = dist_until_refuel;
        this.transport_nodes[name] = transportNode;
    }

    addConnection(nodeA, nodeB, capacity, time) {
        let connection = new Connection(nodeA, nodeB, capacity, time);
        this.connections.push(connection);
    }

    updateTransportNodePosition(name, newLat, newLon) {
        if (this.transport_nodes[name]) {
            this.transport_nodes[name].lat = newLat;
            this.transport_nodes[name].lon = newLon;
        }
    }
}