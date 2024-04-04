from io import BytesIO
import contextily as ctx
import numpy as np
import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from flask import Flask, render_template_string
from matplotlib.animation import HTMLWriter
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

app = Flask(__name__)

# Function to create a graph from the provided nodes and connections
def create_graph(nodes):
    G = nx.Graph()

    # Add nodes with their coordinates
    for node_id, node_info in nodes.items():
        node_type = node_info['type']
        if node_type == 's':
            G.add_node(node_id, pos=(
                node_info['x'], node_info['y']), color='#D4D4D4')
        elif node_type == 'd':
            G.add_node(node_id, pos=(
                node_info['x'], node_info['y']), color='#ACCCE6')
        elif node_type == 'i':
            G.add_node(node_id, pos=(
                node_info['x'], node_info['y']), color='white')

    # Add edges
    for node_id, node_info in nodes.items():
        connections = node_info['connections']
        for connection in connections:
            G.add_edge(node_id, connection)

    return G

nodes = {
    0: {'type': 's', 'x': 126.9731, 'y': 37.5664, 'connections': [1, 2]},
    1: {'type': 'i', 'x': 126.9706, 'y': 37.5654, 'connections': [0, 4, 9]},
    2: {'type': 'i', 'x': 126.9753, 'y': 37.5656, 'connections': [0, 3, 7, 11]},
    3: {'type': 'i', 'x': 126.9774, 'y': 37.5664, 'connections': [2, 17, 19]},
    4: {'type': 'i', 'x': 126.9691, 'y': 37.5651, 'connections': [1, 5, 16]},
    5: {'type': 'i', 'x': 126.9691, 'y': 37.5641, 'connections': [4, 18]},
    6: {'type': 'i', 'x': 126.9729, 'y': 37.5641, 'connections': [0, 7, 18]},
    7: {'type': 'i', 'x': 126.9756, 'y': 37.5641, 'connections': [2, 6, 19]},
    8: {'type': 'i', 'x': 126.9675, 'y': 37.5665, 'connections': [9, 14, 16]},
    9: {'type': 'i', 'x': 126.9704, 'y': 37.5671, 'connections': [1, 8, 10, 13]},
    10: {'type': 'i', 'x': 126.9756, 'y': 37.5671, 'connections': [9, 11, 12]},
    11: {'type': 'i', 'x': 126.9774, 'y': 37.5676, 'connections': [2, 10, 15]},
    12: {'type': 'i', 'x': 126.9755, 'y': 37.5681, 'connections': [10, 13, 15]},
    13: {'type': 'd', 'x': 126.9706, 'y': 37.5686, 'connections': [9, 12]},
    14: {'type': 'd', 'x': 126.9691, 'y': 37.5682, 'connections': [8]},
    15: {'type': 'd', 'x': 126.9774, 'y': 37.5687, 'connections': [11, 12]},
    16: {'type': 'd', 'x': 126.9676, 'y': 37.5681, 'connections': [4, 8, 14]},
    17: {'type': 'd', 'x': 126.9774, 'y': 37.5664, 'connections': [3]},
    18: {'type': 'd', 'x': 126.9676, 'y': 37.5641, 'connections': [5, 6]},
    19: {'type': 'd', 'x': 126.9774, 'y': 37.5641, 'connections': [3, 7]},
}

# Create the graph
G = create_graph(nodes)

# Function to draw the initial graph
def setup_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=500, font_size=8)
    return pos

# Set up the plot
fig, ax = plt.subplots()
pos = setup_graph(G)

# Choose the source node and one destination node for the demo
source_node = 0
destination_node = 19  # Example
paths = [[0, 6, 18], [0, 1, 9, 8, 16], [
    0, 1, 9, 13], [0, 2, 3, 17], [0, 2, 3, 19]]

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

def save_animation_as_string(ani):
    # Use BytesIO to capture the animation's HTML representation as binary data
    animation_bytes_io = BytesIO()
    # Save the animation to the BytesIO buffer with the HTMLWriter
    ani.save(animation_bytes_io, writer=HTMLWriter())
    # Seek to the start of the stream
    animation_bytes_io.seek(0)
    # Return the HTML content as a string
    return animation_bytes_io.getvalue().decode('utf-8')

@app.route('/')
def index():
    plt.close('all')  # Close any existing figures to start fresh

    # You can adjust the size as needed
    fig, ax = plt.subplots(figsize=(10, 10))  # Width and height in inches
    G = create_graph(nodes)
    pos = setup_graph(G)

    # Add the basemap to the Axes instance
    ctx.add_basemap(ax, crs='EPSG:4326',
                    source=ctx.providers.OpenStreetMap.Mapnik)

    # Adjust the plot limits
    min_x = min(node['x'] for node in nodes.values()) - 0.01
    max_x = max(node['x'] for node in nodes.values()) + 0.01
    min_y = min(node['y'] for node in nodes.values()) - 0.01
    max_y = max(node['y'] for node in nodes.values()) + 0.01
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.axis('off')

    # Initialize the dots within the route to ensure they are new for each request
    dots = [ax.plot([], [], 'go', markersize=10)[0] for _ in paths]

    # Update function for the animation
    def update(frame):
        for i, dot in enumerate(dots):
            points = all_points[i]
            if frame < len(points):
                dot.set_data(points[frame])
            else:
                # If the frame exceeds the number of points for this path, hide the dot
                dot.set_data([], [])
        return dots

    # Function to interpolate points between two nodes
    def interpolate_points(p1, p2, num_points=20):
        return list(zip(np.linspace(p1[0], p2[0], num_points),
                        np.linspace(p1[1], p2[1], num_points)))

    # Generate points for each path
    all_points = []
    for path in paths:
        points = []
        for i in range(len(path) - 1):
            start_pos = pos[path[i]]
            end_pos = pos[path[i + 1]]
            # Include the endpoint (end_pos) in the interpolation
            points += interpolate_points(start_pos, end_pos)
        # Add the last point (the node position) to each path
        points.append(end_pos)
        all_points.append(points)

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=max(len(p) for p in all_points),
                                  init_func=lambda: dots, repeat=False, interval=100)

    # Convert the animation to JavaScript HTML format
    animation_jshtml = ani.to_jshtml()

    # CSS to make the map take full width and reduce white space
    custom_css = """
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #animation_container {
            width: 90%;
            height: auto;
            margin: auto;
        }
        .mpl-container {
            width: 100%;
            height: auto;
        }
    </style>
    """

    # Embed the animation HTML in your response
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Path Animation</title>
    {custom_css}
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.7.0/d3.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        #map {
            height: 500px;
        }
    </style>
</head>
<body>
    <h1>Interactive OpenStreetMap</h1>
    <div id="map"></div>
    <div id="animation_container">
        {animation_jshtml}
    </div>
    <script>
        var map = L.map('map').setView([37.5664, 126.9731], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);
    </script>
</body>
</html>"""

    return render_template_string(html_template, animation_jshtml=animation_jshtml)

if __name__ == '__main__':
    app.run(debug=True)
