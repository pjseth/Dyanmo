import math
import requests

class Node:
    def __init__(self, lat, lon, name=None, evacuation_capacity=0, current_population=0, sea_node=False):
        self.lat = lat
        self.lon = lon
        self.name = name or f"({lat},{lon})"
        self.evacuation_capacity = evacuation_capacity
        self.current_population = current_population
        self.connections = {}
        self.sea_node = sea_node

    def is_evacuation_point(self):
        return self.evacuation_capacity > 0

    def euclidean_distance(self, other):
        return math.sqrt((self.lat - other.lat) ** 2 + (self.lon - other.lon) ** 2)

class TransportNode(Node):
    def __init__(self, lat, lon, name=None, evacuation_capacity=0, current_population=0, sea_node=False, aerial=False, velocity=(0, 0), dist_until_refuel=0):
        super().__init__(lat, lon, name, evacuation_capacity, current_population, sea_node)
        self.velocity = velocity
        self.dist_until_refuel = dist_until_refuel
        self.aerial = aerial

    def move(self, time_delta):
        """Update the transport node's position based on its velocity."""
        dlat, dlon = self.velocity
        self.lat += dlat * time_delta
        self.lon += dlon * time_delta
        self.dist_until_refuel -= math.sqrt(dlat**2 + dlon**2) * time_delta

class Graph:
    def __init__(self, api_key):
        self.fixed_nodes = {}
        self.transport_nodes = {}
        self.api_key = api_key

    def get_coordinates(self, address):
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return (latitude, longitude)
        else:
            print(f"Error fetching coordinates for {address}: {data['status']}")
            return None

    def add_fixed_node_by_address(self, address, name=None, evacuation_capacity=0, current_population=0, sea_node=False):
        coords = self.get_coordinates(address)
        if coords:
            self.add_fixed_node(*coords, name, evacuation_capacity, current_population, sea_node)

    def add_fixed_node(self, lat, lon, name=None, evacuation_capacity=0, current_population=0, sea_node=False):
        node = Node(lat, lon, name, evacuation_capacity, current_population, sea_node)
        self.fixed_nodes[name] = node

    def add_transport_node(self, lat, lon, name=None, evacuation_capacity=0, current_population=0, sea_node=False, aerial=False, velocity=(0, 0), dist_until_refuel=0):
        node = TransportNode(lat, lon, name, evacuation_capacity, current_population, sea_node, aerial, velocity, dist_until_refuel)
        self.transport_nodes[name] = node

    def update_edge_weights(self):
        """Update the edge weights (distances) based on current positions of transport nodes."""
        for tname, tnode in self.transport_nodes.items():
            for fname, fnode in self.fixed_nodes.items():
                if (tnode.sea_node and fnode.sea_node) or tnode.aerial:
                    distance = tnode.euclidean_distance(fnode)
                    tnode.connections[fname] = distance

# Example usage:
api_key = "YOUR_GOOGLE_MAPS_API_KEY"
graph = Graph(api_key)
graph.add_fixed_node_by_address("Statue of Liberty, New York", "StatueOfLiberty", sea_node=True)
graph.add_transport_node(40.7138, -74.0070, name="Helicopter1", aerial=True, velocity=(0.001, 0.001))
graph.update_edge_weights()