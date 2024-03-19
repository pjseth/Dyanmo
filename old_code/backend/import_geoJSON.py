import json
import sqlite3

def read_geojson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    conn.execute('''CREATE TABLE IF NOT EXISTS geojson_features (
                    id TEXT PRIMARY KEY, 
                    type TEXT, 
                    properties TEXT, 
                    geometry TEXT)''')
    return conn

def insert_features(conn, features):
    cursor = conn.cursor()
    for feature in features:
        id_value = feature.get('id')
        geom_type = feature['geometry']['type']
        properties = json.dumps(feature['properties'])
        geometry = json.dumps(feature['geometry'])

        cursor.execute('''INSERT INTO geojson_features (id, type, properties, geometry) 
                          VALUES (?, ?, ?, ?)''', (id_value, geom_type, properties, geometry))
    conn.commit()

def main():
    # Path to the GeoJSON file
    geojson_file_path = r'Dyanmo\backend\rail_network.geojson'

    # Read GeoJSON file
    geojson_data = read_geojson(geojson_file_path)

    # Create database and table
    db_conn = create_database('geojson_data.db')

    # Insert GeoJSON features into the database
    insert_features(db_conn, geojson_data['features'])

    db_conn.close()

if __name__ == "__main__":
    main()
