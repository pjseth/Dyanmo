import matplotlib.pyplot as plt
import matplotlib.animation as ani
import networkx as nx
import numpy as np

# Function to create a graph from the provided nodes and connections
def create_graph(nodes):
    G = nx.Graph()
    
    # Add nodes with their coordinates
    for node_id, node_info in nodes.items():
        node_type = node_info['type']
        if node_type == 's':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), color='#D4D4D4')
        elif node_type == 'd':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), color='#ACCCE6')
        elif node_type == 'i':
            G.add_node(node_id, pos=(node_info['x'], node_info['y']), color='white')
    
    # Add edges
    for node_id, node_info in nodes.items():
        connections = node_info['connections']
        for connection in connections:
            G.add_edge(node_id, connection)
    
    return G

# Function to draw the graph
def draw_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    node_colors = [node[1]['color'] for node in G.nodes(data=True)]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
    plt.show()

# Define nodes and their attributes
nodes = {
     0: {'type': 's', 'x': 0, 'y': 0, 'connections': [1, 2]},
    1: {'type': 'i', 'x': -10, 'y': 1, 'connections': [0, 4, 9]},
    2: {'type': 'i', 'x': 10, 'y': 1, 'connections': [0, 3, 7, 11]},
    3: {'type': 'i', 'x': 14, 'y': 1.5, 'connections': [2, 17, 19]},
    4: {'type': 'i', 'x': -20, 'y': 1.5, 'connections': [1, 5, 16]},
    5: {'type': 'i', 'x': -20, 'y': -10, 'connections': [4, 18]},
    6: {'type': 'i', 'x': 0.5, 'y': -10, 'connections': [0, 7, 18]},
    7: {'type': 'i', 'x': 10, 'y': -10, 'connections': [2, 6, 19, 20]},
    8: {'type': 'i', 'x': -15, 'y': 8, 'connections': [9, 14, 16]},
    9: {'type': 'i', 'x': -10, 'y': 8, 'connections': [1, 8, 10, 13]},
    10: {'type': 'i', 'x': -0.5, 'y': 8, 'connections': [9, 11, 12]},
    11: {'type': 'i', 'x': 10, 'y': 8, 'connections': [2, 10, 15]},
    12: {'type': 'i', 'x': -0.5, 'y': 13, 'connections': [10, 13, 15]},
    13: {'type': 'd', 'x': -10, 'y': 16, 'connections': [9, 12]},
    14: {'type': 'd', 'x': -15, 'y': 13, 'connections': [8]},
    15: {'type': 'd', 'x': 10, 'y': 13, 'connections': [11, 12]},
    16: {'type': 'd', 'x': -20, 'y': 8, 'connections': [4, 8, 14]},
    17: {'type': 'd', 'x': 20, 'y': 1.5, 'connections': [3]},
    18: {'type': 'd', 'x': -15.5, 'y': -10, 'connections': [5, 6]},
    19: {'type': 'd', 'x': 14, 'y': -10, 'connections': [3, 7]},
    20: {'type': 'd', 'x': 10, 'y': -15, 'connections': [7]}
}

# Create the graph
G = create_graph(nodes)

# Function to draw the initial graph
def setup_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_size=8)
    return pos

# Set up the plot
fig, ax = plt.subplots()
pos = setup_graph(G)

# Choose the source node and one destination node for the demo
source_node = 0
destination_node = 19  # Example

# Calculate shortest path from source to destination
path = nx.shortest_path(G, source=source_node, target=destination_node)

# Function to interpolate points between two nodes
def interpolate_points(p1, p2, num_points=20):
    return zip(np.linspace(p1[0], p2[0], num_points),
               np.linspace(p1[1], p2[1], num_points))

# Generate the full set of points for the animation
points = []
for i in range(len(path)-1):
    start_pos = pos[path[i]]
    end_pos = pos[path[i+1]]
    points.extend(interpolate_points(start_pos, end_pos))

dot, = plt.plot([], [], 'go', markersize=10)  # Initialize the dot

def init():
    dot.set_data([], [])
    return dot,

# Update function for the animation
def update(frame):
    if frame < len(points):
        dot.set_data(points[frame])
    return dot,

# Create the animation
ani = ani.FuncAnimation(fig, update, frames=range(len(points)), init_func=init,
                        blit=True, repeat=False, interval=50)

plt.show()
