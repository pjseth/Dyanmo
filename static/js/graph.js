class Node {
    constructor(name, lat, lon, current_pop = 0, max_capacity = 0) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.current_pop = current_pop;
        this.max_capacity = max_capacity;  // Maximum capacity at the node
    }
}

class Connection {
    constructor(stationA, stationB, properties, current_pop = 0, max_capacity = 0) {
        this.stationA = stationA;
        this.stationB = stationB;
        this.properties = properties;
        this.current_pop = current_pop;  // Current population on the rail line
        this.max_capacity = max_capacity;  // Maximum capacity of the rail line
    }
}

class Graph {
    constructor() {
        this.stations = {};
        this.connections = [];
    }

    addStation(name, lat, lon, current_pop = 0, max_capacity = 0) {
        this.stations[name] = new Node(name, lat, lon, current_pop, max_capacity);
    }

    addConnection(stationAName, stationBName, properties, current_pop = 0, max_capacity = 0) {
        if (this.stations[stationAName] && this.stations[stationBName]) {
            let connection = new Connection(
                this.stations[stationAName], this.stations[stationBName], 
                properties, current_pop, max_capacity
            );
            this.connections.push(connection);
        }
    }
}

// Export the Graph class for use in other scripts
export { Graph };