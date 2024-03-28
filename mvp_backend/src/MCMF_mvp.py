import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import visualize_graph as visualize

def read_csv_and_create_graph(road_section_data, intersection_data, G):
    """
    Reads a CSV file with specified columns and creates a directed graph.

    Args:
        csv_file (str): Path to the CSV file.
        G (Graph): Graph to read and update.

    Returns:
        nx.DiGraph: Directed graph with edges representing road sections.
    """
    # Read the CSV file
    road_section = pd.read_csv(road_section_data)
    intersection = pd.read_csv(intersection_data)
    intersections = {}

    # Extracting data and store in intersections dict
    for _, intersection in intersection.iterrows():    
        start_node, intersection_node, end_node = str(intersection["start_node"]), str(intersection["intersection_node"]), str(intersection["end_node"])
        capacity = intersection["capacity"]
        delay = intersection["delay"]
        intersections[(start_node, intersection_node, end_node)] = {"capacity":capacity, "delay":delay}

    # Iterate through road data and populate graph
    for _, row in road_section.iterrows():
        start_node = str(int(row["starting node of road section"]))
        end_node = str(int(row["ending node of road section"]))
        travel_time = row["travel time (minutes)"]
        travel_capacity = row["traffic capacity (hundreds of vehicles)"]

        # Add edge with weight (travel time) and capacity (traffic capacity)
        G.add_edge(start_node, end_node, weight=travel_time, capacity=travel_capacity)

    return intersections

def calculate_total_time(G, path, intersections):
    total_time = 0
    for i in range(len(path) - 2):
        start_node = path[i]
        intersection_node = path[i + 1]
        end_node = path[i + 2]

        total_time += G[start_node][intersection_node]['weight']
        total_time += intersections[(start_node, intersection_node, end_node)]['delay']
    
    total_time += G[path[-2]][path[-1]]['weight']
    print(total_time)
    return total_time

def find_possible_destinations(destinations, min_cost_length_and_routes, G, evacuation_flow):
    filtered_routes = {}
    for node, _ in min_cost_length_and_routes[0].items():
        route = min_cost_length_and_routes[1][node]
        if route[-1] in destinations:
            filtered_routes[node] = route

    max_simultaneous_routes = []

    for node, route in filtered_routes.items():
        simultaneous_routes_count = 0
        
        # Iterate over the edges in the route
        update_route = True
        flow_to_next_node = np.inf
        for i in range(len(route) - 1):
            node = route[i]
            next_node = route[i+1]
            
            # Check if the current edge exists in the graph and has enough capacity
            if G[node][next_node]['flow'] <= G[node][next_node]['capacity']:
                flow_to_next_node = min(G[node][next_node]['capacity'], evacuation_flow)
            else:
                # If any edge in the route doesn't have enough capacity, break the loop
                update_route = False
        
        # augment flow along the minimum cost route
        if update_route:
            print("here")
            flow_to_next_node = np.inf
            simultaneous_routes_count += 1
            for i in range(len(route) - 1):
                node = route[i]
                next_node = route[i+1]
                flow_to_next_node = min(G[node][next_node]['capacity'], evacuation_flow)
                G[node][next_node]['flow'] += flow_to_next_node
            
            evacuation_flow -= flow_to_next_node
            max_simultaneous_routes.append(route)

    return max_simultaneous_routes, evacuation_flow

    
# Create a sample network graph (you can replace this with your actual data)
G = nx.DiGraph()

# Add nodes (replace with your actual node labels)
G.add_nodes_from(['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','20'])
source = '0'
destinations = ['13','14','15','16','17','18','19','20']

# Add arcs (replace with your actual arc information)
road_section_data = "../data/road_section_data.csv"

# Add intersection (replace with actual intersection information)
intersection_data = "../data/intersection_capacity.csv"

intersections = read_csv_and_create_graph(road_section_data, intersection_data, G)


# Define the evacuation flow (you can adjust this based on your problem)
evacuation_flow = start_flow = 1000

# Initialize flow on each arc
nx.set_edge_attributes(G, 0, 'flow')

# Initialize augmented route (minimum cost route)
min_cost_route = []
total_time = 0

print(f"Evacuation flow before allocation: {evacuation_flow}")
# Find minimum cost route using Bellman-Ford algorithm
min_cost_length_and_routes = nx.single_source_bellman_ford(G, source=source, weight='weight')



while evacuation_flow > 0:
    # calculate total time passed for simultaneous routes
    # Find all possible min cost destination that can happen simultaneously and augment flow
    simultaneous_routes, evacuation_flow = find_possible_destinations(destinations, min_cost_length_and_routes, G, evacuation_flow)
    curr_time = 0
    for route in simultaneous_routes:
        curr_time = max(curr_time, calculate_total_time(G, route, intersections))
    total_time += curr_time

    # Reset flows to 0 for all edges
    if evacuation_flow == 0:
        break
    for edge in G.edges():
        G.edges[edge]['flow'] = 0

    print(f"Evacuation flow after allocation: {evacuation_flow}")


print(f"Evacuation flow: {evacuation_flow} (remaining flow)")
print(f"Total time: {total_time:.2f} units")
"""print(f"Minimum cost route: {min_cost_route}")"""

# Visualize the network graph (optional)
node_colors = []

# Assign colors to nodes based on whether they are source nodes or destination nodes
for node in G.nodes():
    if node == source:
        node_colors.append('green')  # Color for source nodes
    elif node in destinations:
        node_colors.append('red')  # Color for destination nodes
    else:
        node_colors.append('lightblue')  # Default color

pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=10, font_color='black')
labels = nx.get_edge_attributes(G, 'flow')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Evacuation Network")
plt.show()