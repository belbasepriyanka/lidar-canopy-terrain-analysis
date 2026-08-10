import numpy as np

def canopy_metrics(chm):
    a = np.asarray(chm, dtype=float)
    valid = a[np.isfinite(a) & (a >= 0)]
    return {
        "mean_canopy_height": float(valid.mean()),
        "p95_canopy_height": float(np.percentile(valid,95)),
        "max_canopy_height": float(valid.max()),
        "canopy_cover_gt_2m": float(np.mean(valid > 2.0))
    }
