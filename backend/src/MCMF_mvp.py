import networkx as nx
import pandas as pd
import numpy as np
from data_structures import Vehicle, EvacuationPoint, Route

def read_csv_and_create_graph(road_section_data, intersection_data, G):
    road_section = pd.read_csv(road_section_data)
    intersection = pd.read_csv(intersection_data)
    intersections = {}

    for _, intersection in intersection.iterrows():    
        start_node, intersection_node, end_node = str(intersection["start_node"]), str(intersection["intersection_node"]), str(intersection["end_node"])
        capacity = intersection["capacity"]
        delay = intersection["delay"]
        intersections[(start_node, intersection_node, end_node)] = {"capacity": capacity, "delay": delay}

    for _, row in road_section.iterrows():
        start_node = str(int(row["starting node of road section"]))
        end_node = str(int(row["ending node of road section"]))
        travel_time = row["travel time (minutes)"]
        travel_capacity = row["traffic capacity (hundreds of vehicles)"]

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
        routes_with_flow = []
        
        update_route = True
        flow_to_next_node = np.inf
        for i in range(len(route) - 1):
            node = route[i]
            next_node = route[i+1]
            
            if G[node][next_node]['flow'] <= G[node][next_node]['capacity']:
                flow_to_next_node = min(G[node][next_node]['capacity'], evacuation_flow)
                routes_with_flow.append((node, next_node, flow_to_next_node))
            else:
                update_route = False
                break
        
        if update_route:
            simultaneous_routes_count += 1
            flows = []
            for edge in routes_with_flow:
                node, next_node, flow_to_next_node = edge
                G[node][next_node]['flow'] += flow_to_next_node
                flows.append(flow_to_next_node)
            
            evacuation_flow -= flow_to_next_node
            max_simultaneous_routes.append((route, flows))

    return max_simultaneous_routes, evacuation_flow

def add_unique_route(all_unique_routes, all_unique_route_flows, new_route, flow):
    new_tuple = tuple(new_route)
    if new_tuple not in set(map(tuple, all_unique_routes)):
        all_unique_routes.append(new_route)
        all_unique_route_flows.append(flow)

def assign_vehicles_to_evacuation_points(vehicles, evacuation_points, routes):
    vehicle_assignments = []
    for vehicle in vehicles:
        best_point = None
        best_distance = float('inf')
        for point in evacuation_points:
            distance = calculate_distance(vehicle.location, point.location)
            if distance < best_distance and point.capacity > 0:
                best_distance = distance
                best_point = point
        if best_point:
            best_point.capacity -= vehicle.capacity
            vehicle_assignments.append({
                'vehicle_id': vehicle.vehicle_id,
                'vehicle_type': vehicle.vehicle_type,
                'vehicle_capacity': vehicle.capacity,
                'vehicle_location': vehicle.location,
                'evacuation_point': best_point.point_id,
                'route': find_route_for_vehicle(vehicle.location, best_point.location, routes),
                'distance': best_distance
            })
    return vehicle_assignments

def run_algorithm_with_evacuation_flow(mcmf_dir, total_evacuation_flow, vehicles, evacuation_points):
    G = nx.DiGraph()

    G.add_nodes_from(['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','20'])
    source = '0'
    destinations = ['13','14','15','16','17','18','19','20']

    road_section_data = "../data/road_section_data.csv"
    intersection_data = "../data/intersection_capacity.csv"

    intersections = read_csv_and_create_graph(road_section_data, intersection_data, G)

    evacuation_flow = total_evacuation_flow

    nx.set_edge_attributes(G, 0, 'flow')

    unique_routes_taken = []
    unique_routes_taken_flows = []
    total_time = 0

    min_cost_length_and_routes = nx.single_source_bellman_ford(G, source=source, weight='weight')

    while evacuation_flow > 0:
        route_and_route_flows, evacuation_flow = find_possible_destinations(destinations, min_cost_length_and_routes, G, evacuation_flow)
        simultaneous_routes = [route_info[0] for route_info in route_and_route_flows]
        route_flows = [route_info[1] for route_info in route_and_route_flows]

        curr_time = 0
        for route in simultaneous_routes:
            curr_time = max(curr_time, calculate_total_time(G, route, intersections))
        total_time += curr_time

        if evacuation_flow <= 0:
            break
        for edge in G.edges():
            G.edges[edge]['flow'] = 0

        for route, flow in zip(simultaneous_routes, route_flows):
            add_unique_route(unique_routes_taken, unique_routes_taken_flows, route, flow)

    vehicle_assignments = assign_vehicles_to_evacuation_points(vehicles, evacuation_points, unique_routes_taken)

    return {
        'unique_routes_taken': unique_routes_taken,
        'total_time': total_time,
        'unique_routes_taken_flows': unique_routes_taken_flows,
        'vehicle_assignments': vehicle_assignments
    }


def calculate_distance(location1, location2):
    return np.linalg.norm(np.array(location1) - np.array(location2))

def find_route_for_vehicle(start, end, routes):
    for route in routes:
        if route[0] == start and route[-1] == end:
            return route
    return []


    # print(f"Evacuation flow: {evacuation_flow} (remaining flow)")
    # print(f"Total time: {total_time:.2f} units")
    # print(unique_routes_taken)

    #return {'unique_routes_taken': unique_routes_taken, 'total_time': total_time, 'unique_routes_taken_flows': unique_routes_taken_flows}
    # """print(f"Minimum cost route: {min_cost_route}")"""

    # # Visualize the network graph (optional)
    # node_colors = []

    # # Assign colors to nodes based on whether they are source nodes or destination nodes
    # for node in G.nodes():
    #     if node == source:
    #         node_colors.append('green')  # Color for source nodes
    #     elif node in destinations:
    #         node_colors.append('red')  # Color for destination nodes
    #     else:
    #         node_colors.append('lightblue')  # Default color

    # pos = nx.kamada_kawai_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=10, font_color='black')
    # labels = nx.get_edge_attributes(G, 'flow')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.title("Evacuation Network")
    # plt.show()