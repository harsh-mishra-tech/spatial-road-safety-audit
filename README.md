# Spatial Geometric Risk & Road Safety Audit Engine

An automated spatial analysis pipeline using **Python (OSMnx, GeoPandas, Shapely)** and **QGIS** to evaluate roadway networks proactively using geometric consistency and speed differential models.

## Key Modules
- **Network Ingestion:** Pulls drivable centerline graphs and junction nodes directly from OpenStreetMap and reprojects them to metric UTM coordinates (EPSG:32643).
- **Geometric Curvature Evaluation:** Computes deflection angles across vertices to determine curve radii ($R$).
- **Operating Speed Consistency ($\Delta V_{85}$):** Categorizes segments based on IRC/AASHTO safety criteria.
- **GIS Cartography:** Visualizes hazard hotspots and high-risk curves inside QGIS.

## Risk Criteria
- **Critical Hazard (Sharp Curve):** $R < 80\text{ m}$, predicted $\Delta V_{85} > 20\text{ km/h}$
- **Moderate Risk:** $80\text{ m} \le R < 180\text{ m}$, predicted $\Delta V_{85} \approx 14\text{ km/h}$
- **Low Risk / Tangent:** $R \ge 180\text{ m}$ or straight alignment

## Quickstart
```bash
pip install -r requirements.txt
python extract_corridor.py
python analyze_curves.py