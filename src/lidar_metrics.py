def canopy_metrics(df):
    veg=df[df.is_vegetation==1]
    return {'mean_canopy_height_m':veg.height_agl.mean(),'p95_canopy_height_m':veg.height_agl.quantile(.95),'max_height_m':df.height_agl.max()}
