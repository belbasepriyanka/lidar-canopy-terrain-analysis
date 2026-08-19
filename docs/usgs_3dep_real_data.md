# Real Public-Data Extension — USGS 3DEP LiDAR

This project now includes a real LAS/LAZ ingestion pathway for **USGS 3D Elevation Program (3DEP)** point-cloud data.

## Download a real point cloud

Use the official USGS **LidarExplorer** or **The National Map Downloader** to choose an area of interest and download a 3DEP lidar point-cloud tile. USGS distributes 3DEP lidar point clouds in LAS/LAZ formats; LAZ is the compressed form of LAS.

Official starting points:

- https://www.usgs.gov/tools/lidarexplorer
- https://www.usgs.gov/tools/download-data-maps-national-map
- https://data.usgs.gov/datacatalog/data/USGS%3Ab7e353d2-325f-4fc6-8d95-01254705638a

## Run the real-data script

```bash
pip install -r requirements.txt
python src/real_laz_ingestion.py path/to/your_tile.laz
```

The script reads XYZ, ASPRS classification, and return information; uses class-2 ground points to estimate a simple local ground surface; normalizes heights above ground; and calculates vegetation/canopy metrics.

## Why this matters

The synthetic demo remains useful because anyone can run it immediately. The real-data pathway demonstrates that the same repository can ingest an actual industry-standard point-cloud product rather than only a CSV mock-up.

## Production improvements

For a stronger operational LiDAR workflow, add PDAL-based filtering, robust DTM interpolation, DSM/CHM raster generation, tile-edge handling, CRS/unit checks, vertical-datum documentation, quality-level metadata, and validation against field measurements.

## Data provenance

USGS 3DEP data are public geospatial elevation products. Keep the original project/tile metadata beside any downloaded file so acquisition date, spatial reference, units, quality level, and source project remain traceable.
