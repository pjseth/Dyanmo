import pandas as pd
import geopandas as gpd
import sqlalchemy
from shapely.geometry import shape, LineString
import json
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
import scipy as sp
from pyproj import CRS


# Connect to the SQLite database
engine = sqlalchemy.create_engine('sqlite:///geojson_data.db')

def load_data(query, engine, geom_col):
    df = pd.read_sql(query, engine)
    df[geom_col] = df[geom_col].apply(lambda x: shape(json.loads(x)))  # Convert GeoJSON to geometry objects
    return gpd.GeoDataFrame(df, geometry=geom_col)

# Load data into GeoDataFrames
nodes_gdf = load_data("SELECT * FROM geojson_features WHERE substr(id, 1, 1) = 'n';", engine, 'geometry')
polylines_gdf = load_data("SELECT * FROM geojson_features WHERE substr(id, 1, 1) = 'w';", engine, 'geometry')

def find_nearest_polyline(node, polylines):
    distances = polylines.distance(node.geometry)
    nearest_index = distances.idxmin()
    nearest_polyline = polylines.iloc[nearest_index]
    return nearest_polyline['id']

def traverse_and_sum_lengths(start_polyline_id, polylines_gdf, original_node_id):
    visited = set()  # To keep track of visited polylines
    branches = [[(start_polyline_id, 0)]]  # Initialize branches with start polyline and initial length 0

    final_edges = []  # Store final edges as tuples: (original_node_id, final_node_id, total_length)

    while branches:
        branch = branches.pop(0)
        current_polyline_id, current_length = branch[-1]

        if current_polyline_id in visited:
            continue

        visited.add(current_polyline_id)

        current_polyline = polylines_gdf.loc[polylines_gdf['id'] == current_polyline_id].iloc[0]
        next_length = current_length + current_polyline['length']

        if current_polyline['has_station']:
            # For each associated node, record the edge
            for final_node_id in current_polyline['associated_nodes']:
                final_edges.append((original_node_id, final_node_id, next_length))
        else:
            # Continue traversing
            for adj_id in current_polyline['adjacent_ids']:
                new_branch = branch + [(adj_id, next_length)]
                branches.append(new_branch)

    return final_edges



nodes_gdf['nearest_polyline_id'] = nodes_gdf.apply(lambda x: find_nearest_polyline(x, polylines_gdf), axis=1)
print(nodes_gdf)

polylines_gdf = polylines_gdf.set_crs('epsg:4326')

utm_projection = CRS('epsg:32652')  
polylines_gdf_utm = polylines_gdf.to_crs(utm_projection)

polylines_gdf['length'] = polylines_gdf.geometry.length / 1000
print(polylines_gdf[['id', 'length']])

# Update the database
conn = sqlite3.connect('geojson_data.db')

# Update polyline lengths
for idx, row in polylines_gdf.iterrows():
    conn.execute("UPDATE geojson_features SET length = ? WHERE id = ?", (row['length'], row['id']))

# Update nearest polyline IDs for nodes
for idx, row in nodes_gdf.iterrows():
    conn.execute("UPDATE geojson_features SET nearest_polyline_id = ? WHERE id = ?", (row['nearest_polyline_id'], row['id']))

# Get a set of polyline IDs that are nearest to nodes
nearest_polyline_ids = set(nodes_gdf['nearest_polyline_id'])

# Classify polylines
polylines_gdf['has_station'] = polylines_gdf['id'].apply(lambda x: True if x in nearest_polyline_ids else False)

# Marks if polyline has station
for idx, row in polylines_gdf.iterrows():
    conn.execute("UPDATE geojson_features SET has_station = ? WHERE id = ?", (row['has_station'], row['id']))

# Assuming polylines_gdf is already loaded with LineString geometries
for idx, polyline in polylines_gdf.iterrows():
    # Finding other polylines that touch the current one
    adjacent_polylines = polylines_gdf[polylines_gdf.geometry.touches(polyline.geometry) & (polylines_gdf.index != idx)]
    # Store the IDs or indices of adjacent polylines
    polylines_gdf.at[idx, 'adjacent_ids'] = adjacent_polylines['id'].tolist()

# Assuming polylines_gdf has a column 'adjacent_ids' which are lists of indices
for idx, row in polylines_gdf.iterrows():
    # Convert list of adjacent_ids to a string
    adjacent_ids_str = ','.join(row['adjacent_ids'])
    #print(row['id'] + ": ")
    #print(adjacent_ids_str)

    # Update the database row with the adjacent_ids
    conn.execute("UPDATE geojson_features SET adjacent_ids = ? WHERE id = ?", (adjacent_ids_str, row['id']))

#THIS SECTION CREATES THE ASSOCIATED NODES COLUMN
# Create a dictionary to hold node IDs for each polyline
nodes_per_polyline = {poly_id: [] for poly_id in polylines_gdf['id']}

# Populate the dictionary
for idx, row in nodes_gdf.iterrows():
    nearest_polyline_id = row['nearest_polyline_id']
    if nearest_polyline_id in nodes_per_polyline:
        nodes_per_polyline[nearest_polyline_id].append(row['id'])

# Add this information to polylines_gdf
polylines_gdf['associated_nodes'] = polylines_gdf['id'].map(nodes_per_polyline)

# Update the database with associated nodes information
for idx, row in polylines_gdf.iterrows():
    # Convert list of node IDs to a comma-separated string
    associated_nodes_str = ','.join(row['associated_nodes'])
    
    # Update the database
    conn.execute("UPDATE geojson_features SET associated_nodes = ? WHERE id = ?", (associated_nodes_str, row['id']))

# Initialize a NetworkX Graph
G = nx.Graph()  # or nx.DiGraph() for a directed graph

# Add nodes to the graph
for idx, node in nodes_gdf.iterrows():
    G.add_node(node['id'])

# Assuming nodes_gdf and polylines_gdf are already loaded
for idx, node in nodes_gdf.iterrows():
    original_node_id = node['id']
    start_polyline_id = node['nearest_polyline_id']
    
    edges = traverse_and_sum_lengths(start_polyline_id, polylines_gdf, original_node_id)

    # Process the edges as needed (e.g., adding to a graph or storing in a database)
    # Add edges to the graph
    for edge in edges:
        _, final_node_id, edge_weight = edge
        #print(f"Edge from {original_node_id} to {final_node_id} with weight {edge_weight}")
        G.add_edge(original_node_id, final_node_id, weight=edge_weight)

print(G)
max_weight_edge = max(G.edges(data='weight'), key=lambda x: x[2])
print(f"Edge with the largest weight: {max_weight_edge}")

conn.commit()
conn.close()




# def combine_adjacent_polylines(start_polyline, polylines, nodes, threshold_distance):
#     combined_polylines = [start_polyline]
#     current_polyline = start_polyline

#     while True:
#         # Define logic to find adjacent polyline
#         # This is a placeholder for the logic you need to develop
#         next_polyline = find_next_adjacent_polyline(current_polyline, polylines, nodes, threshold_distance)
        
#         if next_polyline is None:
#             break
        
#         combined_polylines.append(next_polyline)
#         current_polyline = next_polyline

#     return combined_polylines

# def find_next_adjacent_polyline(current_polyline, polylines, nodes, threshold_distance):
#     # Implement logic to find the next adjacent polyline
#     # Consider spatial relationships and the threshold distance
#     # Return the next polyline if found, else return None
#     pass

# combined_edges = []

# for _, node in nodes_gdf.iterrows():
#     start_polyline = node['nearest_polyline']
#     combined_polylines = combine_adjacent_polylines(start_polyline, polylines_gdf, nodes_gdf, threshold_distance)
#     # Add logic to handle combined polylines as an edge
#     combined_edges.append(combined_polylines)

# G = nx.Graph()

# # Add nodes
# for _, node in nodes_gdf.iterrows():
#     G.add_node(node['id'], geometry=node.geometry)

# # Add edges
# # This will depend on how you have combined your polylines and what data you store for each edge
# # Assuming combined_edges is a list of dictionaries with edge information
# for edge in combined_edges:
#     G.add_edge(edge['start_node'], edge['end_node'], length=edge['length'])