import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

# Function to create a graph from the provided nodes and connections
def create_graph(nodes):
    G = nx.Graph()
    
    # Add nodes with their coordinates
    for node_id, node_info in nodes.items():
        node_type = node_info['type']
        if node_type == 's':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), node_type='s')
        elif node_type == 'i':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), node_type='i')
        elif node_type == 'd':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), node_type='d')
    
    # Add edges
    for node_id, node_info in nodes.items():
        connections = node_info['connections']
        for connection in connections:
            G.add_edge(node_id, connection)
    
    return G

# Function to draw the graph
def draw_graph(G, fig, ax):
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw nodes
    node_types = nx.get_node_attributes(G, 'node_type')
    node_colors = ['black' if node_type == 's' else 'blue' if node_type == 'i' else 'white' for node_type in node_types.values()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, ax=ax)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax)
    
    # Retrieve and plot the street network of Seoul from OpenStreetMap
    city = ox.geocode_to_gdf('Seoul, South Korea')
    ox.plot_graph(ox.graph_from_place('Seoul, South Korea'), ax=ax, node_color='none', edge_color='gray', close=False)

# Define nodes and their attributes
nodes = {
    0: {'type': 's', 'x': 37.5665, 'y': 126.978, 'connections': [1, 2]},
    1: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [0, 4, 9]},
    2: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [0, 3, 7, 11]},
    3: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [2, 17, 19]},
    4: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [1, 5, 16]},
    5: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [4, 18]},
    6: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [0, 7, 18]},
    7: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [2, 6, 19, 20]},
    8: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [9, 14, 16]},
    9: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [1, 8, 10, 13]},
    10: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [9, 11, 12]},
    11: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [2, 10, 15]},
    12: {'type': 'i', 'x': 37.5665, 'y': 126.978, 'connections': [10, 13, 15]},
    13: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [9, 12]},
    14: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [8]},
    15: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [11, 12]},
    16: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [4, 8, 14]},
    17: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [3]},
    18: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [5, 6]},
    19: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [3, 7]},
    20: {'type': 'd', 'x': 37.5665, 'y': 126.978, 'connections': [7]}
}

# Create the graph
G = create_graph(nodes)

# Plot the graph with the map background
fig, ax = plt.subplots(figsize=(10, 10))
draw_graph(G, fig, ax)

plt.show()
