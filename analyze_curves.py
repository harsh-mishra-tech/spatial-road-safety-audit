import geopandas as gpd
import numpy as np
import os
from shapely.geometry import LineString

# Path to the extracted vector file
input_path = r"C:\Users\harsh mishra\AppData\Local\Programs\Microsoft VS Code\vapi_corridor_network.gpkg"
output_path = r"C:\Users\harsh mishra\AppData\Local\Programs\Microsoft VS Code\vapi_safety_risk_analyzed.gpkg"

print("Reading road layer...")
roads = gpd.read_file(input_path, layer="roads")

def evaluate_curve(geom):
    """
    Computes cumulative deflection angle and estimates radius of curvature.
    Flags speed consistency drops (ΔV85) using AASHTO/IRC geometric safety criteria.
    """
    if not isinstance(geom, LineString) or len(geom.coords) < 3:
        return 9999.0, "Tangent/Straight", 0.0

    pts = np.array(geom.coords)[:, :2]
    v1 = pts[1:-1] - pts[:-2]
    v2 = pts[2:] - pts[1:-1]

    # Calculate deflection angles between segments
    dot_prod = np.sum(v1 * v2, axis=1)
    norms = np.linalg.norm(v1, axis=1) * np.linalg.norm(v2, axis=1)
    cos_vals = np.clip(dot_prod / (norms + 1e-7), -1.0, 1.0)
    deflections = np.arccos(cos_vals)

    total_deflection_deg = np.sum(np.degrees(deflections))
    arc_length = geom.length

    if arc_length < 10.0 or total_deflection_deg < 15.0:
        return 9999.0, "Low Risk", 0.0

    # R = Arc_Length / Deflection_Radians
    rad_radians = np.radians(total_deflection_deg)
    radius = arc_length / (rad_radians + 1e-7)

    # Risk thresholds based on speed consistency criteria
    if radius < 80.0:
        delta_v85 = 22.0
        risk = "Critical Hazard (Sharp Curve)"
    elif radius < 180.0:
        delta_v85 = 14.0
        risk = "Moderate Risk"
    else:
        delta_v85 = 5.0
        risk = "Low Risk"

    return round(radius, 1), risk, delta_v85

print("Calculating curvature and speed differential metrics...")
metrics = [evaluate_curve(geom) for geom in roads.geometry]

roads['radius_m'] = [m[0] for m in metrics]
roads['risk_cat'] = [m[1] for m in metrics]
roads['delta_v85'] = [m[2] for m in metrics]

# Write out to new layer
roads.to_file(output_path, layer="geometric_risk", driver="GPKG")
print(f"Complete! Saved analyzed layer to:\n{output_path}\n")
print("Risk Breakdown:")
print(roads['risk_cat'].value_counts())