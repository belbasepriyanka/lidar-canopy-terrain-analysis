import pandas as pd
from src.lidar_metrics import canopy_metrics
def test_metrics():
    df=pd.DataFrame({'is_vegetation':[1,1,0],'height_agl':[2.,4.,0.]}); m=canopy_metrics(df); assert m['mean_canopy_height_m']==3
