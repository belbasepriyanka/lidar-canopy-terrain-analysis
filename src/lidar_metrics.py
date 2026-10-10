"""Canopy summaries for gridded heights or normalized point tables."""
import numpy as np


def canopy_metrics(data, threshold_m=2.0):
    if hasattr(data, 'columns'):
        height = data.height_agl.to_numpy(dtype=float)
        vegetation = (data.is_vegetation.to_numpy() == 1) if 'is_vegetation' in data else height > threshold_m
    else:
        height = np.asarray(data, dtype=float).ravel()
        vegetation = height > threshold_m
    valid = np.isfinite(height)
    canopy = height[valid & vegetation]
    maximum = float(height[valid].max()) if valid.any() else 0.0
    cover = float((valid & vegetation).sum() / valid.sum()) if valid.any() else 0.0
    return {'mean_canopy_height_m': float(canopy.mean()) if canopy.size else 0.0,
            'p95_canopy_height_m': float(np.quantile(canopy, .95)) if canopy.size else 0.0,
            'max_height_m': maximum, 'canopy_cover_fraction': cover,
            'max_canopy_height': maximum, 'canopy_cover_gt_2m': cover}
