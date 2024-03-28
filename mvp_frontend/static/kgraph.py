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
    0: {'type': 's', 'y': 37.9045, 'x': 127.0646, 'connections': [1, 2]},
    1: {'type': 'i', 'y': 37.5248, 'x': 126.9674, 'connections': [0, 4, 9]},
    2: {'type': 'i', 'y': 36.9622, 'x': 127.0752, 'connections': [0, 3, 7, 11]},
    3: {'type': 'i', 'y': 35.8939, 'x': 128.5573, 'connections': [2, 17, 19]},
    4: {'type': 'i', 'y': 34.7815, 'x': 127.6698, 'connections': [1, 5, 16]},
    5: {'type': 'i', 'y': 35.2549, 'x': 128.7749, 'connections': [4, 18]},
    6: {'type': 'i', 'y': 34.7815, 'x': 127.6698, 'connections': [0, 7, 18]},
    7: {'type': 'i', 'y': 35.1109, 'x': 129.0443, 'connections': [2, 6, 19, 20]},
    8: {'type': 'i', 'y': 34.7815, 'x': 127.6698, 'connections': [9, 14, 16]},
    9: {'type': 'i', 'y': 34.9841, 'x': 126.3999, 'connections': [1, 8, 10, 13]},
    10: {'type': 'i', 'y': 34.9831, 'x': 127.4726, 'connections': [9, 11, 12]},
    11: {'type': 'i', 'y': 35.1211, 'x': 128.0986, 'connections': [2, 10, 15]},
    12: {'type': 'i', 'y': 33.6116, 'x': 130.3955, 'connections': [10, 13, 15]},
    13: {'type': 'd', 'y': 47.3128, 'x': 122.3273, 'connections': [9, 12]},
    14: {'type': 'd', 'y': 14.6347, 'x': 121.0013, 'connections': [8]},
    15: {'type': 'd', 'y': 37.5680, 'x': 126.9775, 'connections': [11, 12]},
    16: {'type': 'd', 'y': 37.5670, 'x': 126.9690, 'connections': [4, 8, 14]},
    17: {'type': 'd', 'y': 37.5665, 'x': 126.9775, 'connections': [3]},
    18: {'type': 'd', 'y': 37.5640, 'x': 126.9675, 'connections': [5, 6]},
    19: {'type': 'd', 'y': 37.5640, 'x': 126.9775, 'connections': [3, 7]},
    20: {'type': 'd', 'y': 37.5635, 'x': 126.9755, 'connections': [7]}
}

# Create the graph
G = create_graph(nodes)

# Function to draw the initial graph
def setup_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=250, font_size=6)
    return pos

# Set up the plot
fig, ax = plt.subplots()

# Calculate the minimum and maximum coordinates
min_x = min([node_info['x'] for node_info in nodes.values()])
max_x = max([node_info['x'] for node_info in nodes.values()])
min_y = min([node_info['y'] for node_info in nodes.values()])
max_y = max([node_info['y'] for node_info in nodes.values()])

ax.set_xlim(min_x - 10, max_x + 10)
ax.set_ylim(min_y - 15, max_y + 15)

pos = setup_graph(G)

# Choose the source node and one destination node for the demo
source_node = 0
destination_node = 14 

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

# Add OpenStreetMap background
ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

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
