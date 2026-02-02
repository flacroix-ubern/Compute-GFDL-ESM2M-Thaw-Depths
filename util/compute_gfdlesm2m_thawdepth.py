import os
import numpy as np
import netCDF4 as nc
import matplotlib
import matplotlib.pyplot as plt
import string
import xarray
from matplotlib import colors
import sys
from util import calc_thaw_depth

### input variables
#sim = "/oceandata02/model_data/ESM2M_CSCS/AERA3_T30_TYPE2_ENS1/land"
#year_start = 2026
#year_end = 2100
sim_path = str(sys.argv[1])
sim = str(sys.argv[2])
year_start = int(sys.argv[3])
year_end = int(sys.argv[4])

### make year time series
years=np.arange(year_start,year_end)

### Some initialization
### Some indices for later
time_index_thaw = 0  ## set outside loop so that it
month_index = 7 ## for August thaw depth

### Read variables needed for thaw depth initialization
sim_pwd = "{}/{}/land".format(sim_path,sim)
ds = nc.Dataset("{}/land_month_{}.nc".format(sim_pwd,year_start))
longitude = np.squeeze(ds["lon"])
latitude = np.squeeze(ds["lat"])

### initialize thaw depth
thaw_depth = np.zeros((len(years),len(latitude),len(longitude)))
 
### compute thaw depth at every grid point every August
for year in years:
    ### Read in data
    sim_pwd = "{}/{}/land".format(sim_path,sim)
    ds = nc.Dataset("{}/land_month_{}.nc".format(sim_pwd,year_start))
    tsl = np.squeeze(ds["soil_T"]) # soil layer temperature
    time = np.squeeze(ds["time"])
    soil_depth = np.squeeze(ds["zfull_soil"])
    longitude = np.squeeze(ds["lon"])
    latitude = np.squeeze(ds["lat"])

    ### Define maximum thaw depth relevant for vegetation
    max_thawdepth = 5 ## 5m depth is max, otherwise assume no permafrost
    precision = 0.01  ## Precision metric to detect differences in thaw depth

    ### Add nans where they should be (equal or deeper than 5m thaw depths)
    ### limit thaw depth to 5m for first layer
    for lat in np.arange(0,len(latitude)):
        for lon in np.arange(0,len(longitude)):
            if thaw_depth[time_index_thaw,lat,lon] > (max_thawdepth - precision):
                thaw_depth[time_index_thaw,lat,lon] = np.nan

    #### Call compute thaw depth function
    thaw_depth = calc_thaw_depth(thaw_depth,tsl,latitude,longitude,soil_depth,month_index,time_index_thaw,max_thawdepth)
    time_index_thaw = time_index_thaw + 1
    print(time_index_thaw+year_start, "done")

### Compute permafrost area
ds = nc.Dataset("data/gfdlesm2m_area.nc")
area = np.array(ds["cell_area"])

### Compute area
permafrost_area = np.nansum(np.nansum(np.where(thaw_depth[:,:,:]>0,1,np.nan) * area,axis=2),axis=1)

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

thaw_depth_xarray.to_netcdf(path = "output/thawdepth_{}_{}_{}.nc".format(sim,year_start,year_end))
permafrost_area_xarray.to_netcdf(path = "output/permafrostarea_{}_{}_{}.nc".format(sim,year_start,year_end))
permafrostCloss_xarray.to_netcdf(path = "output/permafrostcloss_{}.nc".format(sim,year_start,year_end))
permafrostNloss_xarray.to_netcdf(path = "output/permafrostnloss_{}.nc".format(sim,year_start,year_end))
