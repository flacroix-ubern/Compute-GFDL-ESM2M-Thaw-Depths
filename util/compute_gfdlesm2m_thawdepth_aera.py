import os
import numpy as np
import netCDF4 as nc
import matplotlib
import matplotlib.pyplot as plt
import string
import xarray
from matplotlib import colors

### Thaw Calculation Function



#def function calc_thaw_depth(tsl,lat,lon)
year_start = 2026
year_end = 2300

### make year time series
years=np.arange(year_start,year_end)

### Some initialization 
### some indices for later
time_index_thaw = 0 ## set outside loop so that it
month_index = 7 ## for August thaw depth

### Read variables needed for thaw depth initialization
sim_pwd = "/oceandata02/model_data/ESM2M_CSCS/{}/land".format(sim)
ds = nc.Dataset("{}/land_month_{}.nc".format(sim_pwd,year_start))
longitude = np.squeeze(ds["lon"])
latitude = np.squeeze(ds["lat"])

### initialize thaw depth
thaw_depth = np.zeros((len(years),len(latitude),len(longitude)))

### compute thaw depth at every grid point every August
for year in years:

    ### Read in data
    sim_pwd = "/oceandata02/model_data/ESM2M_CSCS/{}/land".format(sim)
    ds = nc.Dataset("{}/land_month_{}.nc".format(sim_pwd,year))
    tsl = np.squeeze(ds["soil_T"]) # soil layer temperature
    time = np.squeeze(ds["time"])
    soil_depth = np.squeeze(ds["zfull_soil"])
    longitude = np.squeeze(ds["lon"])
    latitude = np.squeeze(ds["lat"])

    ### Define maximum thaw depth relevant for vegetation
    max_thawdepth = 5 ## 5m depth is max, otherwise assume no permafrost
    precision = 0.01  ## Precision metric to detect differences in thaw depth

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

    # limit thaw depth to 5m for first layer
    for lat in np.arange(0,len(latitude)):
        for lon in np.arange(0,len(longitude)):
            if thaw_depth[time_index_thaw,lat,lon] > (max_thawdepth - precision):
                thaw_depth[time_index_thaw,lat,lon] = np.nan

    time_index_thaw = time_index_thaw + 1
    print(time_index_thaw+year_start, "done")

    ### Compute permafrost area
    ds = nc.Dataset("data/gfdlesm2m_area.nc")
    area = np.array(ds["cell_area"])

    ### Compute area
    permafrost_area = np.nansum( np.nansum( np.where( thaw_depth[:,:,:]>0,1,np.nan ) * area,axis=2 ),axis= 1 )

    ### Compute permafrost C and N
    ref_depth = 3   ### depth of data

    ###read dataset
    ds = nc.Dataset("data/SOC_TN_01deg_esm2mgrid.nc")

    ### read C & N storage to 3m
    totalSOC = np.array(ds["SOC"])
    totalSON = np.array(ds["TN"])

    ### Read soil C and N data
    SOC_conc = totalSOC / ref_depth
    SON_conc = totalSON / ref_depth

    ### permafrost content
    permafrostC = SOC_conc * ( 5 - thaw_depth )
    permafrostN = SON_conc * ( 5 - thaw_depth )

    ### permafrost loss
    permafrostCloss = np.nansum( np.nansum(( permafrostC[:,:,:] - permafrostC[0,:,:]) * area, axis=2 ), axis=1 )
    permafrostNloss = np.nansum( np.nansum(( permafrostN[:,:,:] - permafrostN[0,:,:]) * area, axis=2 ), axis=1 )

    #### Write netcdf file
    thaw_depth_xarray = xarray.DataArray(thaw_depth[:,:,:], 
                coords = {"time":years,"lat":latitude,"lon":longitude},                
                dims = ["time","lat","lon"], 
                name = "thaw_depth",attrs={"units":"[m]"})

    permafrost_area_xarray = xarray.DataArray(permafrost_area[:],
                coords = {"time":years},
                dims = ["time"],
                name = "permafrost area",attrs={"units":"[m]"})

    permafrostCloss_xarray = xarray.DataArray(permafrostCloss[:],
                coords = {"time":years},
                dims = ["time"],
                name = "permafrostC loss",attrs={"units":"[m]"})

    permafrostNloss_xarray = xarray.DataArray(permafrostNloss[:],
                coords = {"time":years},
                dims = ["time"],
                name = "permafrostN loss",attrs={"units":"[m]"})

    print(not np.any(thaw_depth[0,:,:]))
    print(not np.any(thaw_depth[1,:,:]))

    thaw_depth_xarray.to_netcdf(path = "output/thawdepth_{}.nc".format(sim))
    permafrost_area_xarray.to_netcdf(path = "output/permafrostarea_{}.nc".format(sim))
    permafrostCloss_xarray.to_netcdf(path = "output/permafrostcloss_{}.nc".format(sim))
    permafrostNloss_xarray.to_netcdf(path = "output/permafrostnloss_{}.nc".format(sim))
