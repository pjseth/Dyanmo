import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

def read_csv_and_create_graph(csv_file, G):
    """
    Reads a CSV file with specified columns and creates a directed graph.

    Args:
        csv_file (str): Path to the CSV file.
        G (Graph): Graph to read and update.

    Returns:
        nx.DiGraph: Directed graph with edges representing road sections.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Iterate through rows and add edges to the graph
    for _, row in df.iterrows():
        start_node = str(int(row["starting node of road section"]))
        end_node = str(int(row["ending node of road section"]))
        travel_time = row["travel time (minutes)"]
        travel_capacity = row["traffic capacity (hundreds of vehicles)"]

        # Add edge with weight (travel time) and capacity (traffic capacity)
        G.add_edge(start_node, end_node, weight=travel_time, capacity=travel_capacity)

    return G

# Create a sample network graph (you can replace this with your actual data)
G = nx.DiGraph()

# Add nodes (replace with your actual node labels)
G.add_nodes_from(['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','20'])
source = '0'
destinations = ['13','14','15','16','17','18','19','20']

# Add arcs (replace with your actual arc information)
csv_file_path = "../data/road_section_data.csv"
read_csv_and_create_graph(csv_file_path, G)

# Define the evacuation flow (you can adjust this based on your problem)
evacuation_flow = 200

# Initialize flow on each arc
nx.set_edge_attributes(G, 0, 'flow')

# Initialize augmented route (minimum cost route)
min_cost_route = []

for dest in destinations:
    while evacuation_flow > 0:
        # Find minimum cost route using Bellman-Ford algorithm
        min_cost_length_and_routes = nx.single_source_bellman_ford(G, source=source, weight='weight')
        current_min_cost_route = min_cost_length_and_routes[1][dest]

        # Augment flow along the minimum cost route
        for i in range(len(current_min_cost_route) - 1):
            node = current_min_cost_route[i]
            next_node = current_min_cost_route[i + 1]
            flow_to_next_node = min(G[node][next_node]['capacity'], evacuation_flow)
            G[node][next_node]['flow'] += flow_to_next_node
            evacuation_flow -= flow_to_next_node

        # Update augmented route
        min_cost_route += current_min_cost_route

    # Calculate total time (sum of travel times along the augmented route)
    total_time = sum(G[u][v]['flow'] * G[u][v]['weight'] for u, v in G.edges())

print(f"Evacuation flow: {evacuation_flow} (remaining flow)")
print(f"Total time: {total_time:.2f} units")
print(f"Minimum cost route: {min_cost_route}")

# Visualize the network graph (optional)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightblue', font_size=10, font_color='black')
labels = nx.get_edge_attributes(G, 'flow')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Evacuation Network")
plt.show()
