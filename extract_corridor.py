import osmnx as ox
import geopandas as gpd

print("Connecting to OpenStreetMap...")

# Study area: Vapi - Daman Road / NH 48 arterial junction area
# Coordinates: Lat 20.3720, Lon 72.9150 (Vapi corridor)
latitude = 20.3720
longitude = 72.9150
search_radius = 2000  # 2.0 km radius

# Fetch drivable road network
G = ox.graph_from_point((latitude, longitude), dist=search_radius, network_type='drive')

# Convert graph to GeoDataFrames
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Reproject to metric UTM projection (EPSG:32643 - UTM Zone 43N)
# This converts degrees to meters for precise curve and length measurements
gdf_edges_metric = gdf_edges.to_crs(epsg=32643)
gdf_nodes_metric = gdf_nodes.to_crs(epsg=32643)

# Save to GeoPackage format for QGIS
output_file = "vapi_corridor_network.gpkg"
gdf_edges_metric.to_file(output_file, layer="roads", driver="GPKG")
gdf_nodes_metric.to_file(output_file, layer="intersections", driver="GPKG")

print(f"Extraction successful! Saved to {output_file}")
print(f"Total road links extracted: {len(gdf_edges_metric)}")
print(f"Total intersection nodes extracted: {len(gdf_nodes_metric)}")