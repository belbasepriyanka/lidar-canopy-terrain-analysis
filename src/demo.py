from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from lidar_metrics import canopy_metrics

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "outputs").mkdir(exist_ok=True)
rng = np.random.default_rng(101)
n_ground = 3500
xg = rng.uniform(0,100,n_ground)
yg = rng.uniform(0,100,n_ground)
zg = 0.025*xg + 0.012*yg + rng.normal(0,.08,n_ground)

n_veg = 4500
xv = rng.uniform(0,100,n_veg)
yv = rng.uniform(0,100,n_veg)
terrain = 0.025*xv + 0.012*yv
canopy = 2 + 13*np.exp(-((xv-48)**2+(yv-55)**2)/(2*24**2)) + rng.gamma(1.5,1.0,n_veg)
zv = terrain + canopy

pts = pd.DataFrame({
    "x": np.r_[xg,xv],
    "y": np.r_[yg,yv],
    "z": np.r_[zg,zv],
    "classification": np.r_[np.repeat("ground",n_ground), np.repeat("vegetation",n_veg)]
})
pts.to_csv(ROOT/"data"/"synthetic_lidar_points.csv", index=False)

gx, gy = np.mgrid[0:100:180j, 0:100:180j]
dtm = griddata((xg,yg), zg, (gx,gy), method="linear")
dsm = griddata((xv,yv), zv, (gx,gy), method="linear")
chm = dsm - dtm
metrics = canopy_metrics(chm)
(ROOT/"outputs"/"canopy_metrics.json").write_text(json.dumps(metrics, indent=2))
plt.figure(figsize=(6,5.2))
plt.imshow(chm.T, origin="lower", extent=[0,100,0,100])
plt.colorbar(label="Canopy height (m)")
plt.xlabel("X"); plt.ylabel("Y"); plt.title("Synthetic LiDAR Canopy Height Model")
plt.tight_layout(); plt.savefig(ROOT/"outputs"/"canopy_height_model.png", dpi=180); plt.close()
print(metrics)
