Description 

This code processes geographic data stored in an SQLite database and runs an Mixed Integer Linear Programming Model to allow for evacuation route customization in Korea. The script utilizes pandas, geopandas, sqlalchemy, shapely, json, networkx, matplotlib, sqlite3, scipy, and pyproj libraries to handle data manipulation, spatial operations, and database connectivity.

The backend supports integrating the supply data (assumed to be given to the NEO teams in Korea during a time of emergency evacuation) into the program to run its MILP Model into an OpenStreetMap API. The front end is a web application that projects the OpenStreetMap API as an HTML page. It provides API endpoints for updating and retrieving information about railroads from the SQLite database.

Installation 

On the repo, simply follow to path of the frontend static folder
Run the script: python3 server.py
Connect to localhost: 8000 to see results
