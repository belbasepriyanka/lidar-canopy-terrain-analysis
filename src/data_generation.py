import numpy as np
import pandas as pd
def generate_lidar(seed=22,n=6000):
    rng=np.random.default_rng(seed); x=rng.uniform(0,100,n); y=rng.uniform(0,100,n); ground=4+.025*x+.015*y+.5*np.sin(x/10); veg=rng.random(n)<.62; canopy=np.where(veg,rng.gamma(3,2.2,n),0); z=ground+canopy+rng.normal(0,.12,n)
    return pd.DataFrame({'x':x,'y':y,'z':z,'ground_z':ground,'is_vegetation':veg.astype(int),'height_agl':np.maximum(0,z-ground)})
