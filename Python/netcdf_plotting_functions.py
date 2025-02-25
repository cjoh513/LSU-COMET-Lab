# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:13:58 2024

@author: Philip_comet_lab
"""
#Necessary libraries.  These are also imported in the function itself too so you don't need to worry about importing these
#But if you intend to use these functions you'll probably want to go ahead and install the below libraries
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"General Observed variable"
def obs_var (file_path,
             var_name,
             lat_name,
             lon_name,
             timestep=None,
             vertical=None,
             lat_id_ext=None,
             lon_id_ext=None,
             lat_deg_ext=None,
             lon_deg_ext=None,
             ):
    
    """
    file_path  = path to netcdf file.
    var_name   = string, file defined name for variable of interest.  
    lat_name   = file defined lat name.
    lon_name   = file defined lon name.
    timestep   = Optional, if set, grabs the variable of interest from the set timestep id
    vertical   = Optional, if set, grabs the variable of interest from the set vertical id
    lat_id_ext = Optional, Can define a 2 item list (e.g., [93, 160]) the outputted variable of interest is set to go between these instead of full extent
    lon_id_ext = Optional, same as lat_id_ext but for longitude
    lat_deg_ext= Optional, finds the nearest lat id from a provided lat degree
    lon_deg_ext = Optional, same as lat_deg_ext
    """

    #imports
    from netCDF4 import Dataset
    import numpy as np
    file = Dataset(file_path)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    "defining lats and lons"
    #if its a 1d lat lon
    if len(file[lat_name].dimensions) == 1:
        if lat_id_ext!=None:
            lat_id_ext = lat_id_ext
        elif lat_deg_ext != None:
            bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
            bottom_dist, top_dist = ((file[lat_name][:] - bottom_lat)**2)**0.5, ((file[lat_name][:] - top_lat)**2)**0.5
            lat_id_ext = [np.where(bottom_dist == bottom_dist.min())[0][0], np.where(top_dist == top_dist.min())[0][0]]
        else:
            lat_id_ext = [0,len(file[lat_name][:])]
            
            
        if lon_id_ext != None:
            lon_id_ext = lon_id_ext
        elif lon_deg_ext != None:
            left_lon, right_lon = lon_deg_ext[0],lon_deg_ext[1]
            left_dist,right_dist = ((file[lon_name][:] - left_lon)**2)**0.5, ((file[lon_name][:] - right_lon)**2)**0.5
            lon_id_ext = [np.where(left_dist == left_dist.min())[0][0], np.where(right_dist == right_dist.min())[0][0]]
        else:
            lon_id_ext = [0,len(file[lon_name][:])]
        

        lats,lons = file[lat_name][lat_id_ext[0]:lat_id_ext[1]], file[lon_name][lon_id_ext[0]:lon_id_ext[1]]
    
    
    
    
    #if it's a 2d lat lons
    if len(file[lat_name].dimensions) == 2:
        if lat_id_ext != None:
            lat_id_ext = lat_id_ext
        elif lat_deg_ext != None:
            bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
            bottom_dist,top_dist = ((file[lat_name][:,:] - bottom_lat)**2)**0.5, ((file[lat_name][:,:] - top_lat)**2)**0.5
            lat_id_ext = [np.where(bottom_dist == bottom_dist.min())[0][0], np.where(top_dist == top_dist.min())[0][0]]
            print("lats",lat_id_ext)
        else:
            lat_id_ext = [0,len(file[lat_name][:,0])]
            
            
        if lon_id_ext != None:
            lon_id_ext = lon_id_ext
        elif lon_deg_ext != None:
            left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]    
            left_dist,right_dist = ((file[lon_name][:,:] - left_lon)**2)**0.5, ((file[lon_name][:,:] - right_lon)**2)**0.5
            lon_id_ext = [np.where(left_dist == left_dist.min())[1][0], np.where(right_dist == right_dist.min())[1][0]]
            print("lons",lon_id_ext)
        else:
            lon_id_ext = [0,len(file[lon_name][0,:])]
        
        lats,lons = file[lat_name][ min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ], file[lon_name][ min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]
        print(lats.shape,lons.shape)
    
    
    
    #if it's 3d lat lons (i.e., if there's time in the first slot)
    if len(file[lat_name].dimensions) == 3:
        if lat_id_ext != None:
            lat_id_ext = lat_id_ext
        elif lat_deg_ext != None:
            bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
            bottom_dist,top_dist = ((file[lat_name][0,:,0] - bottom_lat)**2)**0.5, ((file[lat_name][0,:,0] - top_lat)**2)**0.5
            lat_id_ext = [np.where(bottom_dist == bottom_dist.mine())[0][0], np.where(top_dist == top_dist.min())[0][0]]
        else:
            lat_id_ext = [0,len(file[lat_name][0,:,0])]
            
            
        if lon_id_ext != None:
            lon_id_ext = lon_id_ext
        elif lon_deg_ext != None:
            left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]
            left_dist,right_dist = ((file[lon_name][0,0,:] - left_lon)**2)**0.5, ((file[lon_name][0,0,:] - right_lon)**2)**0.5
            lon_id_ext = [np.where(left_dist == left_dist.min())[1][0], np.where(right_dist == right_dist.min())[1][0]]
        else:
            lon_id_ext = [0,len(file[lon_name][0,0,:])]
            
            
        lats,lons = file[lat_name][ 0, min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ], file[lon_name][ 0, min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]
    
        
    #if for whatever reason there's more than 3 dimensions.
    if len(file[lat_name].dimensions) > 3:  
        print("Too many dimensions in the lat,lon for this function to handle. Dimensions:",len(file[lat_name].dimensions))
    """"""""""""""""""""""""""""""""""""""""""""""""""""""  
    
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    "Getting the variable of interest"
    #variable with or without a timestep defined
    if timestep != None and vertical == None:
        print("timestep, no vert")
        var = file[var_name][ timestep,           min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]

    elif timestep == None and vertical != None:
        print("no timestep, vert")
        var = file[var_name][ vertical,           min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]
        
    elif timestep != None and vertical != None:
        print("both")
        var = file[var_name][ timestep, vertical, min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]
    else:
        print("none")
        var = file[var_name][                     min(lat_id_ext):max(lat_id_ext), min(lon_id_ext):max(lon_id_ext) ]
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    file.close()
    return(var,lons,lats)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 









""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Getting Precip Variable"
#An older version of the previous function
def obs_precipitation(file_path,precip_variable_name):
    file = Dataset(file_path)
    lons,lats = file['lon'][:],file['lat'][:]
    precip = file[precip_variable_name][:,:]
    return (precip,lons,lats)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

    
    





""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Plotting"
#Older, less extensive version of the same function on the "wrfout_plotting_functions.py" file
def obs_plotting(lons,lats,
                 plotted,
                 contour_range,
                 tick_range,
                 extent,
                 title,
                 ):
    title = title
    proj = ccrs.PlateCarree()
    lons,lats = lons,lats
    contour_range = contour_range
    tick_range = tick_range
    fig = plt.figure(figsize=(12,8))
    ax = plt.axes(projection=proj)
    
    plt.contourf(lons,lats,
                 plotted,
                 contour_range,
                 extend='max',
                 )
    
    cbar = plt.colorbar(orientation = 'horizontal',
                        ticks = tick_range,
                        pad = 0.05,
                        )
    #ax.set_extent(extent)
    ax.coastlines()
    ax.add_feature(cfeature.STATES, linewidth=0.4)
    g1 = ax.gridlines(draw_labels=True,linewidth=0.5,linestyle='--')
    g1.xlabels_top=False
    g1.ylabels_right=False
    ax.set_title(title)

    plt.show()
    plt.clf()
""""""""""""""""""""""""""""""""""""""""""""""""""""""


# "Test"
# extent = "None"
# path = r"I:/observed_precip/MSD_5_year_acc_precip_obs_2.nc"
# obs_precip = obs_precipitation(path,"NLDAS_FORA0125_H_2_0_Rainf")[0] / 5
# lons,lats = obs_precipitation(path,"NLDAS_FORA0125_H_2_0_Rainf")[1],obs_precipitation(path,"NLDAS_FORA0125_H_2_0_Rainf")[2]
# obs_plotting(lons,lats,
#              obs_precip,
#              np.arange(0,4001,500),
#              np.arange(0,4001,500),
#              extent,
#              "Mean Obs Precip",
#              )


""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Creating NC File"
def new_nc_obs(new_file_path,
               lons,lats,
               new_file_title,
               new_var_name,
               new_var_std_name,
               var_to_write,
               ):
    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating File"
    new_file = Dataset(new_file_path,mode="w",format='NETCDF4')
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating Dimensions"
    y_dim = new_file.createDimension('y',len(lats))
    x_dim = new_file.createDimension('x',len(lons))
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    new_file.title = new_file_title
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating Variables"
    lat = new_file.createVariable('lat',np.float64,'y')
    ###takes three arguments for create variable: name, type, and dimension. Not sure why theres's a comma after the dimension argument but following tutorial so...
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'

    lon = new_file.createVariable('lon',np.float64,'x')### my assumption is this comma indicates there are no other dimensions associated with it
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'

    new_precip_var = new_file.createVariable(new_var_name,np.float64,('y','x'))
    new_precip_var.standard_name = new_var_std_name
    """"""""""""""""""""""""""""""""""""""""""""""""""

    new_file['lat'][:] = lats
    new_file['lon'][:] = lons
    new_file[new_var_name][:,:]  = var_to_write

    new_file.close()
""""""""""""""""""""""""""""""""""""""""""""""""""""""


""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Paul's finding nearest latlon"
def nearest_2d(lat_array,lon_array,ll_coords):
    targ_lat, targ_lon = ll_coords[0], ll_coords[1]
    lat_dist = lat_array - targ_lat
    lon_dist = lon_array - targ_lon  
    dist = (lat_dist**2 + lon_dist**2)**0.5
    idx = np.where(dist == dist.min())[0][0]
    return idx
""""""""""""""""""""""""""""""""""""""""""""""""""""""

