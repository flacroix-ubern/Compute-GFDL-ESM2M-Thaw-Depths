import numpy as np

### Thaw Calculation Function
def calc_thaw_depth(thaw_depth,tsl,latitude,longitude,soil_depth,month_index,time_index_thaw,max_thawdepth):
    for lat in np.arange(0,len(latitude)):
        for lon in np.arange(0,len(longitude)):
            if tsl[month_index,0,lat,lon]<1000:
                for depth_index in np.arange(0,len(soil_depth)):
                    if tsl[month_index,depth_index,lat,lon]>273.15:
                        thaw_depth[time_index_thaw,lat,lon] = soil_depth[depth_index]
                    elif depth_index>0 and tsl[month_index,depth_index,lat,lon]<=273.15 and tsl[month_index,depth_index-1,lat,lon]>273.15:
                        thaw_depth[time_index_thaw,lat,lon] = thaw_depth[time_index_thaw,lat,lon] + (soil_depth[depth_index] - soil_depth[depth_index-1]) / (tsl[month_index,depth_index,lat,lon] - tsl[month_index,depth_index-1,lat,lon]) * (tsl[month_index-1,depth_index,lat,lon] - 273.15)
                # limit thaw depth to 5m
                if thaw_depth[0,lat,lon]>max_thawdepth and time_index_thaw>0:
                    thaw_depth[time_index_thaw,lat,lon]=np.nan
                elif (thaw_depth[time_index_thaw,lat,lon]>max_thawdepth and thaw_depth[0,lat,lon]<max_thawdepth):
                    thaw_depth[time_index_thaw,lat,lon]=max_thawdepth
    return thaw_depth[:,:,:]
