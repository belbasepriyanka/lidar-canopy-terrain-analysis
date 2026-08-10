import sys
from pathlib import Path
import numpy as np
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from lidar_metrics import canopy_metrics

def test_canopy_metrics():
    m = canopy_metrics(np.array([[0,1],[3,5]], dtype=float))
    assert m["max_canopy_height"] == 5.0
    assert 0 <= m["canopy_cover_gt_2m"] <= 1
