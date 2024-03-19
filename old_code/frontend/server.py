from flask import Flask, jsonify, send_from_directory, request
import sqlite3
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/rail_network.geojson')
def rail_network_geojson():
    return send_from_directory(app.root_path, 'data/rail_network.geojson')

@app.route('/api/updatePopulation', methods=['POST'])
def update_population():
    data = request.json
    station_id = data['id']
    print(data)
    new_population = data['newValue']
    
    # Update the database with the new population
    conn = sqlite3.connect(os.path.join(app.root_path, 'data/railroads.db'))
    cursor = conn.cursor()
    cursor.execute("UPDATE railroads SET current_pop = ? WHERE id = ?", (new_population, station_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "id": station_id, "new_population": new_population})

@app.route('/api/updateCapacity', methods=['POST'])
def update_capacity():
    data = request.json
    station_id = data['id']
    new_capacity = data['newValue']

    # Update the database with the new capacity
    conn = sqlite3.connect(os.path.join(app.root_path, 'railroads.db'))
    cursor = conn.cursor()
    cursor.execute("UPDATE railroads SET max_capacity = ? WHERE id = ?", (new_capacity, station_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "id": station_id, "new_max_capacity": new_capacity})

@app.route('/api/updatePersonnelNeeded', methods=['POST'])
def update_personnel_needed():
    data = request.json
    station_id = data['id']
    new_personnel_needed = data['newValue']

    # Update the database with the new capacity
    conn = sqlite3.connect(os.path.join(app.root_path, 'railroads.db'))
    cursor = conn.cursor()
    cursor.execute("UPDATE railroads SET personnel_needed = ? WHERE id = ?", (new_personnel_needed, station_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "id": station_id, "new_personnel_needed": new_personnel_needed})

@app.route('/api/updatePersonnelPresent', methods=['POST'])
def update_personnel_present():
    data = request.json
    print(data)
    station_id = data['id']
    new_personnel_present = data['newValue']

    # Update the database with the new capacity
    conn = sqlite3.connect(os.path.join(app.root_path, 'railroads.db'))
    cursor = conn.cursor()
    cursor.execute("UPDATE railroads SET personnel_present = ? WHERE id = ?", (new_personnel_present, station_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "id": station_id, "new_personnel_present": new_personnel_present})

@app.route('/api/updateTransport', methods=['POST'])
def update_transport():
    data = request.json
    station_id = data['id']
    new_transport = data['newValue']

    # Update the database with the new capacity
    conn = sqlite3.connect(os.path.join(app.root_path, 'railroads.db'))
    cursor = conn.cursor()
    cursor.execute("UPDATE railroads SET transport = ? WHERE id = ?", (new_transport, station_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "id": station_id, "new_transport": new_transport})

def get_capacity_data():
    # Assuming railroads.db is in the same directory as server.py
    conn = sqlite3.connect(os.path.join(app.root_path, 'railroads.db'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, current_pop, max_capacity, personnel_needed, personnel_present, transport FROM railroads")
    data = {id: {"current_population": current_pop, "max_capacity": max_cap, "personnel_needed": personnel_needed, "personnel_present": personnel_present, "transport": transport} for id, current_pop, max_cap, personnel_needed, personnel_present, transport in cursor.fetchall()}
    conn.close()
    return data

@app.route('/api/capacities')
def capacities():
    data = get_capacity_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
