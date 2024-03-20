import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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

    for _, intersection in intersection.iterrows():    
        # Add turnings as edges
        turnings = intersection["turnings"]
        capacity = intersection["capacity"]
        delay = intersection["delay"]
    
        # Add turnings as edges
        for turn in turnings.split(","):
        # Extracting the start node, intersection node, and end node from the string representation of the tuple
            turn = turn.strip()  # Remove leading/trailing spaces
            if turn.startswith("(") and turn.endswith(")"):
                start_node, intersection_node, end_node = map(int, turn[1:-1].split(","))
                start_node = str(start_node)
                intersection_node = str(intersection_node)
                end_node = str(end_node)
                G.add_edge(start_node, intersection_node, capacity=capacity, delay=delay)
                G.add_edge(intersection_node, end_node, capacity=capacity, delay=delay)



    # Iterate through rows and add edges to the graph
    for _, row in road_section.iterrows():
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
road_section_data = "../data/road_section_data.csv"

# Add intersection (replace with actual intersection information)
intersection_data = "../data/intersection_capacity.csv"

read_csv_and_create_graph(road_section_data, intersection_data, G)


# Define the evacuation flow (you can adjust this based on your problem)
evacuation_flow = 200

# Initialize flow on each arc
nx.set_edge_attributes(G, 0, 'flow')

# Initialize augmented route (minimum cost route)
min_cost_route = []

for dest in destinations:
    if evacuation_flow > 0:
        # Find minimum cost route using Bellman-Ford algorithm
        min_cost_length_and_routes = nx.single_source_bellman_ford(G, source=source, weight='weight')
        current_min_cost_route = min_cost_length_and_routes[1][dest]

        # Augment flow along the minimum cost route
        for i in range(len(current_min_cost_route) - 1):
            node = current_min_cost_route[i]
            next_node = current_min_cost_route[i + 1]
            
            # Check if the edge is a road section or intersection turning
            if next_node not in destinations:
                # Augment flow based on road section capacity
                flow_to_next_node = min(G[node][next_node]['capacity'], evacuation_flow)
                G[node][next_node]['flow'] += flow_to_next_node
            else:
                # Find the intersection node
                intersection_node = next_node
                
                # Determine the outgoing edge from the intersection
                intersection_edges = list(G.out_edges(intersection_node))
                out_edge = None
                for edge in intersection_edges:
                    if edge[0] == node:
                        out_edge = edge
                        break
                
                # Augment flow based on intersection capacity
                if out_edge:
                    flow_to_next_node = min(G[out_edge[0]][out_edge[1]]['capacity'], evacuation_flow)
                    G[out_edge[0]][out_edge[1]]['flow'] += flow_to_next_node
                else:
                    # No valid out edge found, raise an error or handle the situation
                    pass

            evacuation_flow -= flow_to_next_node


        # Update augmented route
        min_cost_route += current_min_cost_route

    # Calculate total time (sum of travel times along the augmented route)
    total_time = sum(G[u][v]['flow'] * G[u][v]['weight'] for u, v in G.edges())

print(f"Evacuation flow: {evacuation_flow} (remaining flow)")
print(f"Total time: {total_time:.2f} units")
print(f"Minimum cost route: {min_cost_route}")

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