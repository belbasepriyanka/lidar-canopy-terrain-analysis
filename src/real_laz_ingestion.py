"""Read a real LAS/LAZ point cloud and compute simple canopy-height metrics.

Designed for public USGS 3DEP files downloaded through The National Map / LidarExplorer.
Requires laspy and a LAZ backend such as lazrs.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import laspy


def read_las_laz(path: str | Path) -> pd.DataFrame:
    las = laspy.read(path)
    df = pd.DataFrame({
        'x': np.asarray(las.x),
        'y': np.asarray(las.y),
        'z': np.asarray(las.z),
        'classification': np.asarray(las.classification),
        'return_number': np.asarray(las.return_number),
        'number_of_returns': np.asarray(las.number_of_returns),
    })
    return df


def ground_normalize(df: pd.DataFrame, cell_size: float = 5.0) -> pd.DataFrame:
    """Simple grid-based normalization using ASPRS ground-class points (class 2).

    This is an educational baseline, not a replacement for production-quality
    terrain modeling with PDAL/Whitebox/LAStools or a hydrologically conditioned DTM.
    """
    out = df.copy()
    xmin, ymin = out.x.min(), out.y.min()
    out['gx'] = np.floor((out.x - xmin) / cell_size).astype(int)
    out['gy'] = np.floor((out.y - ymin) / cell_size).astype(int)
    ground = out[out.classification == 2].groupby(['gx','gy'])['z'].median().rename('ground_z')
    out = out.join(ground, on=['gx','gy'])
    out['height_agl'] = out['z'] - out['ground_z']
    return out


def canopy_metrics(df: pd.DataFrame) -> dict:
    valid = df['height_agl'].dropna()
    veg = valid[valid > 2.0]
    return {
        'points': int(len(df)),
        'normalized_points': int(valid.size),
        'vegetation_points_gt_2m': int(veg.size),
        'mean_canopy_height_m': float(veg.mean()) if len(veg) else 0.0,
        'p95_canopy_height_m': float(veg.quantile(0.95)) if len(veg) else 0.0,
    }


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input_laz', help='Path to a USGS 3DEP .laz or .las file')
    args = p.parse_args()
    points = read_las_laz(args.input_laz)
    normalized = ground_normalize(points)
    print(canopy_metrics(normalized))
