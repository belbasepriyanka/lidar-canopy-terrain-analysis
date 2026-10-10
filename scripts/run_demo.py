"""Generate a gridded synthetic point cloud and canopy-height surfaces."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.real_laz_ingestion import ground_normalize
from src.lidar_metrics import canopy_metrics
for name in ['data','results','figures']:(ROOT/name).mkdir(exist_ok=True)
rng=np.random.default_rng(42);y,x=np.mgrid[:40,:40];terrain=5+.04*x+.02*y
height=np.maximum(0,15*np.exp(-((x-18)**2+(y-23)**2)/150)+rng.normal(0,.7,x.shape))
ground=pd.DataFrame({'x':x.ravel()*2,'y':y.ravel()*2,'z':terrain.ravel(),
 'classification':2,'return_number':1,'number_of_returns':1})
veg=ground.copy();veg['z']+=height.ravel();veg['classification']=5
points=pd.concat([ground,veg],ignore_index=True)
normalized=ground_normalize(points,cell_size=2)
chm=normalized[normalized.classification==5].height_agl.to_numpy().reshape(40,40)
normalized.to_csv(ROOT/'data/synthetic_normalized_points.csv',index=False)
metrics=canopy_metrics(chm);metrics['data_type']='synthetic';metrics['grid_cell_size_m']=2
(ROOT/'results/canopy_metrics.json').write_text(json.dumps(metrics,indent=2))
np.savez_compressed(ROOT/'results/synthetic_surfaces.npz',dtm=terrain,dsm=terrain+chm,chm=chm)
fig,axes=plt.subplots(1,2,figsize=(10,4));im=axes[0].imshow(chm,extent=[0,80,0,80]);fig.colorbar(im,ax=axes[0],label='Height m');axes[0].set_title('Synthetic canopy height model')
axes[1].hist(chm.ravel(),bins=25);axes[1].set(title='Synthetic height distribution',xlabel='Height m',ylabel='Cells')
fig.tight_layout();fig.savefig(ROOT/'figures/canopy_demo.svg');plt.close(fig)
print(json.dumps(metrics,indent=2))
