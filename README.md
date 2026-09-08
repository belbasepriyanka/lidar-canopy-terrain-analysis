# Urban Tree Canopy Assessment Using LiDAR & Multispectral Remote Sensing

**Florida International University, Modesto Maidique Campus + Tamiami Park, Miami-Dade County, Florida**  
**Project completed: 2025**  
**Presented to a management team at Florida International University**

This applied geospatial project used **USGS 3DEP LiDAR point-cloud data** and **NAIP four-band multispectral imagery** to map urban tree canopy, estimate canopy height, classify major land-cover types, and identify areas where tree-cover expansion could support campus planning and green-infrastructure decisions.

The project combines **3D structural information from LiDAR** with **spectral vegetation information from multispectral imagery**. A Random Forest classifier was then used to separate tree canopy, grass/low vegetation, impervious surfaces, and water.

## Project Highlights

- Study area: **FIU Modesto Maidique Campus and Tamiami Park**
- Approximate study extent: **67.5 ha (~167 acres)**
- LiDAR: **USGS 3DEP Quality Level 2**, approximately **8 returns/m²**
- Multispectral imagery: **NAIP 4-band RGB + NIR**, approximately **0.3 m resolution**
- GIS environment: **ArcGIS Pro 3.3**
- Tree-canopy extraction: **LiDAR CHM + NDVI fusion**
- Land-cover model: **Random Forest**
- Estimated urban tree canopy: **35.2%**
- Overall classification accuracy: **96.5%**
- Kappa coefficient: **0.953**
- 5-fold cross-validation accuracy: **97.2%**
- Tree-canopy F1 score: **96.0%**

## Why This Project

Urban tree canopy is important for campus and city planning because trees influence shade, heat exposure, stormwater interception, habitat connectivity, and the quality of outdoor spaces. The goal of this project was to move beyond a simple vegetation map and build a workflow that could distinguish **tall woody vegetation from grass and built structures**.

LiDAR provided the vertical structure needed to estimate height, while NAIP imagery provided the spectral information needed to identify photosynthetically active vegetation.

## Data Sources

| Dataset | Source | Use in Project |
|---|---|---|
| LiDAR point cloud | USGS 3D Elevation Program (3DEP), QL2 | DSM, DTM, canopy height and structural information |
| NAIP imagery | USDA Farm Service Agency | RGB/NIR imagery, NDVI and spectral features |
| Vector reference data | OpenStreetMap | Spatial reference and contextual mapping |

## Processing Workflow

```text
USGS 3DEP LiDAR
        |
        +--> First returns --> DSM
        |
        +--> Ground returns, Class 2 --> DTM
                                       |
                                       v
                               CHM = DSM - DTM
                                       |
NAIP RGB + NIR --> NDVI --------------+
                                       |
                                       v
                         CHM + NDVI canopy mask
                                       |
                                       v
                         Random Forest classification
                                       |
                                       v
                           Urban Tree Canopy Map
```

### 1. LiDAR Point-Cloud Processing

LiDAR returns were converted to raster elevation surfaces in ArcGIS Pro.

- **DSM, Digital Surface Model:** generated from first returns so that trees and buildings were represented in the surface elevation.
- **DTM, Digital Terrain Model:** generated from ASPRS **Class 2 ground returns** to represent bare-earth elevation.
- **CHM, Canopy Height Model:** calculated as:

```text
CHM = DSM - DTM
```

A height threshold of approximately **2 m** was used to identify candidate tall vegetation.

### 2. NDVI Mapping

NAIP red and near-infrared bands were used to calculate NDVI:

```text
NDVI = (NIR - Red) / (NIR + Red)
```

NDVI provided the spectral vegetation signal needed to separate vegetation from most non-vegetated urban surfaces.

### 3. LiDAR + Multispectral Fusion

Neither LiDAR height nor NDVI alone was sufficient for reliable tree-canopy extraction.

- NDVI alone can confuse **trees with grass or other green surfaces**.
- Height alone can confuse **trees with buildings and other tall structures**.

The project therefore combined both conditions:

```text
Candidate Tree Canopy = NDVI > 0.25 AND CHM > 2 m
```

This fusion step retained pixels that were both **spectrally vegetated** and **structurally tall**.

### 4. Random Forest Land-Cover Classification

The classification workflow used a Random Forest model with a multi-layer feature stack containing:

1. Red
2. Green
3. Blue
4. Near Infrared
5. NDVI
6. NDWI
7. CHM height
8. Canopy roughness
9. CHM × NDVI interaction

The project configuration used **200 decision trees**, with training and validation samples distributed across the four target classes.

### 5. Accuracy Assessment

Classification performance was evaluated using an independent test subset and standard classification metrics, including:

- confusion matrix
- overall accuracy
- Kappa coefficient
- precision
- recall
- F1 score
- 5-fold cross-validation

## Main Results

| Land-Cover Class | Estimated Coverage |
|---|---:|
| **Tree Canopy** | **35.2%** |
| Grass / Low Vegetation | 28.6% |
| Impervious Surface | 24.8% |
| Water | 11.4% |

### Classification Performance

| Metric | Result |
|---|---:|
| Overall accuracy | **96.5%** |
| Kappa coefficient | **0.953** |
| 5-fold CV accuracy | **97.2%** |
| Tree-canopy F1 score | **96.0%** |

The analysis identified continuous tree corridors around campus walkways and park edges while also highlighting impervious and low-vegetation areas that could be examined for future canopy-expansion opportunities.

## Decision-Support Value

The final canopy and land-cover products were designed to support conversations around:

- campus tree-canopy management
- green-infrastructure planning
- prioritization of potential planting areas
- heat and shade planning
- stormwater and environmental management
- long-term vegetation monitoring

I presented this work to a **management team at Florida International University** as an example of how LiDAR and multispectral remote sensing can translate geospatial data into practical planning information.

## Tools & Skills Demonstrated

**GIS & Remote Sensing**
- ArcGIS Pro 3.3
- Spatial Analyst
- Image Classification Wizard
- Raster Calculator / Map Algebra
- LAS Dataset tools
- LiDAR point-cloud processing
- multispectral remote sensing
- NDVI / NDWI

**LiDAR**
- LAS point clouds
- ASPRS return classification
- DSM generation
- DTM generation
- Canopy Height Model generation
- height thresholding
- canopy-structure interpretation

**Machine Learning & Validation**
- Random Forest
- feature engineering
- training / test sampling
- cross-validation
- confusion matrix
- Kappa coefficient
- precision, recall and F1 score

**Applied Geospatial Analysis**
- urban tree canopy mapping
- land-cover classification
- environmental decision support
- GIS visualization
- technical presentation to non-specialist stakeholders

## Limitations

The original project was designed as an applied remote-sensing assessment rather than a formal field inventory. Important limitations include:

- imagery represents a single acquisition period rather than multi-year canopy dynamics
- a fixed CHM threshold can include some large shrubs or exclude recently pruned trees
- green roofs or rooftop vegetation can occasionally satisfy both spectral and height criteria
- the reported accuracy depends on the validation sample
- no independent on-ground GPS validation campaign was completed

Future work should include independent field validation, multi-year change detection, species-level mapping using UAV or hyperspectral data, and analysis of shade or canopy equity.

## Repository Structure

```text
lidar-canopy-terrain-analysis/
├── README.md
├── data/
├── docs/
├── figures/
├── notebooks/
├── results/
├── scripts/
├── src/
└── tests/
```

### Reproducible Public-Data Extension

This repository also contains a reproducible LiDAR processing demonstration that can ingest public **USGS 3DEP LAS/LAZ** files using Python.

- [`src/real_laz_ingestion.py`](src/real_laz_ingestion.py) provides a real LAS/LAZ ingestion pathway.
- [`docs/usgs_3dep_real_data.md`](docs/usgs_3dep_real_data.md) documents public-data acquisition and provenance.
- `laspy` and `lazrs` are used for point-cloud reading.

The Python demonstration is a **reproducibility extension** of the portfolio repository. It should not be interpreted as the exact ArcGIS Pro workflow used to produce every result reported in the 2025 FIU project.

## Data Transparency

The project results above are drawn from the original FIU Urban Tree Canopy assessment and presentation. Large source LiDAR and NAIP datasets are not committed to this repository. Public data should be downloaded directly from the relevant USGS and USDA repositories when reproducing the workflow.

## Author

**Priyanka Belbase**  
Remote Sensing Scientist | Geospatial Data Scientist | GIS & GeoAI | LiDAR | Machine Learning | Earth Observation

- GitHub: [belbasepriyanka](https://github.com/belbasepriyanka)
- LinkedIn: [Priyanka Belbase](https://www.linkedin.com/in/priyanka-belbase/)
- Google Scholar: [Publications](https://scholar.google.com/citations?user=bkSmlQ8AAAAJ)

---

**Keywords:** LiDAR, point cloud, urban tree canopy, canopy height model, DSM, DTM, CHM, NAIP, NDVI, Random Forest, ArcGIS Pro, remote sensing, GIS, urban forestry, land-cover classification, geospatial machine learning
