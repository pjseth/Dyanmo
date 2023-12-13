import json
import math
import sqlite3

def calculate_distance(lat1, lng1, lat2, lng2):
    return math.sqrt((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2)

def min_per_rail(station, railroad):
    for coord in json.loads(railroad[4]):
        min_val = math.inf
        dist = calculate_distance(station[3], station[2], coord[1], coord[0])
        min_val = min(min_val, dist)
    return min_val

def internal_dist(railroad):
    coordinates = json.loads(railroad[4])  # Assuming railroad[4] contains the line_data in JSON format
    total_distance = 0

    for i in range(len(coordinates) - 1):
        lat1, lng1 = coordinates[i]
        lat2, lng2 = coordinates[i + 1]
        total_distance += calculate_distance(lat1, lng1, lat2, lng2)

    return float(total_distance)

def find_two_closest_lines(station, railroads):
    min1 = float('inf')
    min2 = float('inf')
    min1_id = None
    min2_id = None
    
    for railroad in railroads:
        dist = min_per_rail(station, railroad)
        if dist < min1:
            min2 = min1
            min2_id = min1_id
            min1 = dist
            min1_id = railroad[0]
        elif dist < min2:
            min2 = dist
            min2_id = railroad[0]
    
    return min1_id, min2_id

# # Example data
# lines = [
#     {"id": "way/997991459", "line_data": "[[127.8430029, 37.3461749], [127.8438429, 37.345603], [127.8439663, 37.3455189]]"},
#     {"id": "way/997991458", "line_data": "[[127.6191912, 37.4827872], [127.6134138, 37.4863013]]"},
#     # ... add other lines here ...
# ]
# station = {"id": "node/10165830852", "latitude": 36.0821954, "longitude": 126.7084727}
# stations = [station]

def update_adjacency(conn, line_ids):
    cursor = conn.cursor()
    for line_id in line_ids:
        if line_id is not None:
            cursor.execute("UPDATE railroads SET adjacency = True WHERE id = ?", (line_id,))
    conn.commit()

def update_internal_dist(conn, railroads):
    cursor = conn.cursor()
    for railroad in railroads:
        dist = internal_dist(railroad)
        cursor.execute("UPDATE railroads SET internal_dist = ? WHERE id = ?", (dist, railroad[0]))
    conn.commit()

db_path = r'Dyanmo\frontend\railroads.db'
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

station_query = "SELECT * FROM railroads WHERE line_data IS NULL"
rail_query = "SELECT * FROM railroads WHERE longitude IS NULL"

# Execute the query
cursor.execute(station_query)
stations = cursor.fetchall()

cursor.execute(rail_query)
railroads = cursor.fetchall()


# Finding the two closest lines to the 
adj_matrix = {}
for station in stations:
    closest_lines = find_two_closest_lines(station, railroads)
    adj_matrix[station[0]] = [closest_lines[0], closest_lines[1]]
    update_adjacency(conn, closest_lines)
    #print(f"The two closest lines to station {station[0]} are {closest_lines[0]} and {closest_lines[1]}")

update_internal_dist(conn, railroads)


# Close the database connection
conn.close()
print(adj_matrix)