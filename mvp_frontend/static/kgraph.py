import matplotlib.pyplot as plt
import matplotlib.animation as ani
import networkx as nx
import numpy as np
import contextily as ctx

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

# Define nodes and their attributes with adjusted coordinates
nodes = {
    0: {'type': 's', 'x': 126.9730, 'y': 37.5665, 'connections': [1, 2]},
    1: {'type': 'i', 'x': 126.9705, 'y': 37.5655, 'connections': [0, 4, 9]},
    2: {'type': 'i', 'x': 126.9755, 'y': 37.5655, 'connections': [0, 3, 7, 11]},
    3: {'type': 'i', 'x': 126.9775, 'y': 37.5665, 'connections': [2, 17, 19]},
    4: {'type': 'i', 'x': 126.9690, 'y': 37.5650, 'connections': [1, 5, 16]},
    5: {'type': 'i', 'x': 126.9690, 'y': 37.5640, 'connections': [4, 18]},
    6: {'type': 'i', 'x': 126.9730, 'y': 37.5640, 'connections': [0, 7, 18]},
    7: {'type': 'i', 'x': 126.9755, 'y': 37.5640, 'connections': [2, 6, 19, 20]},
    8: {'type': 'i', 'x': 126.9675, 'y': 37.5670, 'connections': [9, 14, 16]},
    9: {'type': 'i', 'x': 126.9705, 'y': 37.5670, 'connections': [1, 8, 10, 13]},
    10: {'type': 'i', 'x': 126.9755, 'y': 37.5670, 'connections': [9, 11, 12]},
    11: {'type': 'i', 'x': 126.9775, 'y': 37.5675, 'connections': [2, 10, 15]},
    12: {'type': 'i', 'x': 126.9755, 'y': 37.5680, 'connections': [10, 13, 15]},
    13: {'type': 'd', 'x': 126.9705, 'y': 37.5685, 'connections': [9, 12]},
    14: {'type': 'd', 'x': 126.9675, 'y': 37.5680, 'connections': [8]},
    15: {'type': 'd', 'x': 126.9775, 'y': 37.5680, 'connections': [11, 12]},
    16: {'type': 'd', 'x': 126.9690, 'y': 37.5670, 'connections': [4, 8, 14]},
    17: {'type': 'd', 'x': 126.9775, 'y': 37.5665, 'connections': [3]},
    18: {'type': 'd', 'x': 126.9675, 'y': 37.5640, 'connections': [5, 6]},
    19: {'type': 'd', 'x': 126.9775, 'y': 37.5640, 'connections': [3, 7]},
    20: {'type': 'd', 'x': 126.9755, 'y': 37.5635, 'connections': [7]}
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
paths = [[0, 6, 18], [0, 1, 9, 8, 16], [0, 1, 9, 13], [0, 2, 3, 17], [0, 2, 3, 19]]

# Function to interpolate points between two nodes
def interpolate_points(p1, p2, num_points=20):
    return zip(np.linspace(p1[0], p2[0], num_points),
               np.linspace(p1[1], p2[1], num_points))

# Generate points for each path
all_points = []
for path in paths:
    points = []
    for i in range(len(path) - 1):
        start_pos = pos[path[i]]
        end_pos = pos[path[i + 1]]
        points.extend(interpolate_points(start_pos, end_pos))
    all_points.append(points)

dots = [plt.plot([], [], 'go', markersize=10)[0] for _ in range(len(paths))]  # Initialize the dots

def init():
    for dot in dots:
        dot.set_data([], [])
    return dots

# Update function for the animation
def update(frame):
    for i, dot in enumerate(dots):
        points = all_points[i]
        if frame < len(points):
            dot.set_data(points[frame])
    return dots

# Add Korean OpenStreetMap background
ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

# Create the animation
ani = ani.FuncAnimation(fig, update, frames=max(len(points) for points in all_points), init_func=init,
                        blit=True, repeat=False, interval=50)

plt.show()
