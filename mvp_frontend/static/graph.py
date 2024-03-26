import matplotlib.pyplot as plt
import matplotlib.animation as ani
import networkx as nx

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

# Draw the graph
# draw_graph(G)

# Choose the source node and one destination node for the demo
source_node = 0
destination_node = 19  # Example

# Calculate shortest path from source to destination
path = nx.shortest_path(G, source=source_node, target=destination_node)

# Function to draw the initial graph
def setup_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_size=8)
    return pos

# Set up the plot
fig, ax = plt.subplots()
pos = setup_graph(G)

# Add a dot at the source node position
dot, = plt.plot(pos[source_node][0], pos[source_node][1], 'go', markersize=10)  # 'go' for green dot

def update(frame):
    # Frame is the index of the current position in the path
    if frame < len(path):
        node = path[frame]
        dot.set_data(pos[node][0], pos[node][1])
    return dot,

# Create animation
animate = ani.FuncAnimation(fig, update, frames=range(len(path)), blit=True, repeat=False)

plt.show()
