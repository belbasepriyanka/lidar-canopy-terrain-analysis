# LiDAR Canopy & Terrain Analysis

A recruiter-ready LiDAR demonstration covering point-cloud structure, ground normalization, canopy-height metrics, visualization, and reproducible code.

> Public data in this repository are synthetic point-cloud samples for demonstration.

## Demo metrics
- Points: **6,000**
- Vegetation fraction: **61.22%**
- Mean canopy height: **6.59 m**
- 95th percentile canopy height: **13.79 m**

![Canopy map](figures/canopy_height_map.svg)
![Height distribution](figures/height_distribution.svg)

## Run
```bash
pip install -r requirements.txt
python scripts/run_demo.py
python -m pytest -q
```

## Transfer to real data
Replace the sample CSV with LAS/LAZ-derived points or add a `laspy`/PDAL ingestion step; the normalized-height and canopy-metric logic remains the same.
