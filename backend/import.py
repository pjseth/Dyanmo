import json
import sqlite3

def get_english_name(properties):
    return properties.get('name:en') or properties.get('name')

def get_id(feature):
    return feature.get('id')

def read_geojson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding here
        return json.load(file)

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute('''CREATE TABLE IF NOT EXISTS railroads (
                    id TEXT, name TEXT, longitude REAL, latitude REAL, 
                    line_data TEXT, current_pop INTEGER, max_capacity INTEGER, adjacency BOOLEAN)''')
    return conn

def insert_railroad_names(conn, names):
    cursor = conn.cursor()
    for entry in names:
        # Insert data based on feature type
        cursor.execute('''INSERT INTO railroads (id, name, longitude, latitude, 
                       line_data, current_pop, max_capacity, adjacency) VALUES 
                       (?, ?, ?, ?, ?, 100, 1000, FALSE)''', entry)
    conn.commit()

def main():
    geojson_data = read_geojson(r'Dyanmo\backend\rail_network.geojson')
    db_conn = create_database('railroads.db')

    railroad_names = []
    for feature in geojson_data['features']:
        id_value = get_id(feature)
        name_value = feature['properties'].get('name:en') or feature['properties'].get('name')
        print(id_value)

        if feature['geometry']['type'] == 'Point':
            longit, latit = feature['geometry']['coordinates']
            railroad_names.append((id_value, name_value, longit, latit, None))
        elif feature['geometry']['type'] == 'LineString':
            # Convert line coordinates to a string or a suitable format
            line_data = str(feature['geometry']['coordinates'])
            railroad_names.append((id_value, name_value, None, None, line_data))

    insert_railroad_names(db_conn, railroad_names)
    db_conn.close()

if __name__ == "__main__":
    main()
