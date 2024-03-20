import geopandas as gpd
import fiona
from shapely.geometry import LineString, Point

# Define a function to parse OSM data and extract roads
def extract_roads(osm_file):
    roads = []
    with fiona.open(osm_file, 'r', layer='lines') as src:
        for feature in src:
            if 'highway' in feature['properties']:
                road = {
                    'id': feature['id'],
                    'geometry': LineString(feature['geometry']['coordinates']),
                    'tags': feature['properties']
                }
                roads.append(road)
    return roads

# Path to your OSM file
osm_file = 'south-korea-latest.osm.pbf'

# Extract roads from OSM data
roads = extract_roads(osm_file)

# Convert extracted roads to GeoDataFrame
roads_gdf = gpd.GeoDataFrame(roads)
