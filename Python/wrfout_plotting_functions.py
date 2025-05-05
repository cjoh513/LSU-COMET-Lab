# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:04:41 2024

@author: Philip_comet_lab
"""
#Below are the libraries used for these functions.  They are imported at each function so you don't need to worry about importing them yourself
#But... If you're going to use a function, make sure the library is installed.
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
from datetime import datetime, timedelta



""""""""""""""""""""""""""""""""""""""""""""""""""""""
def wrf_precipitation(start_file_path,  end_file_path=None,
                      start_timestep=0, end_timestep=-1,
                      lat_id_ext=None,  lon_id_ext=None,
                      lat_deg_ext=None, lon_deg_ext=None,
                      ):     ###This version means I don't have to manually do the I_rain values each time I plot wrf precip. It checks the file for it
    """"
    This is specifically for collecting WRF precipitation.  This also means that it requires a 2-dimensional lat lon. 
    If You're looking for a generic netCDF array-variable grab (or don't have a 2D lat/lon) try the top function in the "nonwrf_plotting_functions.py" file.
    Extracts Accumulated Precipitation and lat lon grid for the precipitation varibale from wrfout.nc files between two timesteps.  You can use the below arguments to create a window within the array (e.g., if you only wanted to see a rectangular portion of the southeastern U.S. instead of the entire CONUS array)
    start_file_path: Required. The first file to extract precipitation from.  e.g., start_file_path = r"F:\MSD_2096_middle\wrfout_d01_2096-08-01_12%3A00%3A00.nc"
    end_file_path:   Optional. If unspecified, defaults to the same file path as the start_file_path
    start_timestep:  Optional. If unspecified, defaults to the first timestep of the file
    end_timestep:    Optional. If unspecified, defaults to the last timestep of the start_file or end_file (if specified) file
    lat_id_ext:      Optional. Allows for extraction of a horizontal slice between two latitude indexes. (e.g., lat_id_ext=[bottom id, top id], or lat_id_ext=[93,134]).  If unspecified, defaults to collecting every lat value
    lon_id_ext:      Optional. Same as lat_id_ext except for longitude instead of latitude
    lat_deg_ext:     Optional. Providing a degrees north latitude value, a sub-function finds the nearest latitude index/cell. e.g., lat_deg_ext=[bottom degree North, top degree North], or lat_deg_ext = [30.2735, 48.7]
    My recommendation: if you're creating a sub-window of an array and you're using a dataset with non-uniform grid cells (e.g., Daymet or anything on a Lamber-conformal conic grid), using the indexes is preferable than the degree search.  
    This is because the varying 
    """    
    #imports
    from netCDF4 import Dataset
    import numpy as np ##for the find_ids function below (.min())

    #Whether or not you're using two precip files
    if end_file_path == None:
        end_file_path = start_file_path
        
    #Sets up the lattitude portion of the window either in indexes or degrees north
    if lat_id_ext != None:
        lat_id_ext = lat_id_ext
    elif lat_deg_ext != None:
        bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
        bottom_dist, top_dist = ((Dataset(start_file_path)['XLAT'][0,:,:]  - bottom_lat)**2)**0.5, ((Dataset(start_file_path)['XLAT'][0,:,:]  - top_lat)**2)**0.5   ###finds root error.  ((array - target value)squared)squareroot
        lat_id_ext = [np.where(bottom_dist == bottom_dist.min())[0][0],np.where(top_dist == top_dist.min())[0][0]]  ### [0][0] lats
    else:
        lat_id_ext=[0,len(Dataset(start_file_path)['XLAT'][0,:,0])]  
  
    #Sets up the longitude portion of the window either in indexes or degrees east
    if lon_id_ext != None:
        lon_id_ext = lon_id_ext
    elif lon_deg_ext != None:
        left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]
        left_dist, right_dist = ((Dataset(start_file_path)['XLONG'][0,:,:] - left_lon)**2)**0.5,   ((Dataset(start_file_path)['XLONG'][0,:,:] - right_lon)**2)**0.5
        lon_id_ext = [np.where(left_dist == left_dist.min())[1][0],np.where(right_dist == right_dist.min())[1][0]]  ### [1][0] lons
    else:
        lon_id_ext=[0,len(Dataset(start_file_path)['XLONG'][0,0,:])]
    
    
    
    #Start and end data and lats and lons
    start_file = Dataset(start_file_path)
    end_file = Dataset(end_file_path)
    lons,lats = start_file['XLONG'][0,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]], start_file['XLAT'][0,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
    
    
    #Whether there is a convective parameterization or not
    if 'I_RAINNC' in start_file.variables:
        start_irain_nc = start_file['I_RAINNC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   # Buckets gridscale preicp (parameterization)
        start_rain_nc  = start_file[  'RAINNC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #         gridscale precip (parameterization)
        start_irain_c  = start_file[ 'I_RAINC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   # Buckets convective precip (non-parameterization)
        start_rain_c   = start_file[   'RAINC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #         convective precip (non-parameterization)
        start_nc_total = ((start_irain_nc * 100) + start_rain_nc)
        start_c_total  = ((start_irain_c * 100) + start_rain_c)
        start_total = start_nc_total + start_c_total
        
        end_irain_nc = end_file['I_RAINNC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_rain_nc  = end_file[  'RAINNC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_irain_c  = end_file[ 'I_RAINC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_rain_c   = end_file[   'RAINC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_nc_total = ((end_irain_nc * 100) + end_rain_nc)
        end_c_total  = ((end_irain_c * 100) + end_rain_c)
        end_total = end_nc_total + end_c_total
        
        total = end_total - start_total
    else: 
        start_rain_nc = start_file['RAINNC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        start_rain_c  = start_file[ 'RAINC'][start_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        start_total = start_rain_nc + start_rain_c
        
        end_rain_nc = end_file['RAINNC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_rain_c  = end_file[ 'RAINC'][end_timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        end_total = end_rain_nc + end_rain_c
        
        total = end_total - start_total
        
    start_file.close()   
    end_file.close()
    return(total,lons,lats)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotting(
             lons=None,lats=None,
             plotted=None,
             contour_range=None,
             tick_range=None,
             colorbar=True,
             cmap='viridis',
             extent=None,
             title="",
             save_path=None,
             projection = ccrs.PlateCarree(),
             land_sea=False,
             patch = None,
             ):
    
    """
    This is my universal contour-fill plotting function.  I largely use it when I'm plotting a variable from WRF files, but
    it'll handle any 2d variable that you provide lat and lons for.  
    Each argument is optional because I also use this to create a generic map over a domain or to add a patch to it to identify domain regions
    lons:          Array.               If unspecified it'll show the general global map from cartopy.  You can use the extent argument to zoom in too.  
    lats:          Array.               Same as lons but for latitude.  If you specify one you should specify the other
    plotted:       Array.               The 2d array for whatever variable you wwant to plot the contour graphic for
    contour_range: 3-item list.         [start, end, increment], [0,1005,100].  Sets the contour range for the contour fill for whatever. from a start to an end at an increment. If you have a "plotted" argument, you need to specify this and tick_range
    tick_range:    3-item list.         Functions the same as the contour_range, but this one specifies the colorbar tick range.
    colorbar:      Truth statemet.      True=colorbar is plotted, false it is not.  Will only show if plotted!=None
    cmap:          string.              Specify which colormap you want.
    extent:        4-item list.         [left, right, bottom, top].  Sets the extent of the grpahic, but doesn't alter data in any way.  without it, the graph defaults the extents to the edges of the plotted data
    title:         string.              Sets the title of the graph if desired.
    save_path:     1- or 2-item list.   [path to directory to save(e.g., r"F:\MSD_2096_middle"), file name without .png(e.g., file_name)]. the example would result in a file saved as r"F:\MSD_2096_middle/file_name.png".  if only a one item list, it must be the directory path and the function will save the files name as the graphic title.
    projection:    cartopy prjoection.  Defaults to Plate Carree, but this can be specified 
    land_sea:      Truth statement.     If set to True, the land and sea made by cartopy will have colors. usually not useful for a contour plot, but when making a generic map or for including patches it can add a good look to the graphic.  This is just an aesthetics options
    patch:         4-item list.         [left, right, bottom, top].  function calculates the necessary height and width automatically when you provide the edge inputs.  for user input purposes, this operates exactly like the extent argument.  This applies a red patch.  as it stands now you'll need to manually alter the function to change the colors
    """
    
    
    #imports
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import numpy as np
    import matplotlib.patches as mpatches
    
    #Set the more static variables
    title = title
    lons,lats = lons,lats
    
    #Set the ticks and contours.  if you're 
    if contour_range !=None:
        contour_range = np.arange(contour_range[0],contour_range[1],contour_range[2])
    if tick_range != None:
        tick_range = np.arange(tick_range[0],tick_range[1],tick_range[2])
        
    #Set the figure up
    fig = plt.figure(figsize=(12,8))
    ax = plt.axes(projection=projection)
    
    #plot the contour variable if presented
    if plotted is not None:
        plt.contourf(lons,lats,
                     plotted,
                     contour_range,
                     extend='max',
                     cmap=cmap,
                     )
        if colorbar==True:
            cbar = plt.colorbar(orientation = 'horizontal',
                                ticks = tick_range,
                                pad = 0.05,
                                )       
    #set extent if wanted
    if extent != None:
        ax.set_extent(extent)
        
    #Set coastlines and if you want the land and sea to have color
    ax.coastlines()
    if land_sea==True:
        ax.add_feature(cfeature.STATES, linewidth=0.4,facecolor=cfeature.COLORS['land'])
        ax.add_feature(cfeature.OCEAN, linewidth=0.4,facecolor=cfeature.COLORS['water'])
        #ax.add_feature(cfeature.RIVERS,edgecolor='green')
    else:
        ax.add_feature(cfeature.STATES, linewidth=0.4)
        
    #Set the patch
    #It works by finding the lower left corner then setting a width and height.  the setting of a width is annoying so i have it set where you just give the left and right side and subtract them to get the width
    if patch != None:
        ax.add_patch(mpatches.Rectangle(xy=[patch[0],patch[2]],
                                            width=patch[1]-patch[0],
                                            height=patch[3]-patch[2],
                                            edgecolor='red',
                                            facecolor="None",
                                            alpha=1,
                                            linewidth=2,
                                            transform=projection)
                     )
        
    #set gridlines/latlon labels
    g1 = ax.gridlines(draw_labels=True,linewidth=0.5,linestyle='--')
    g1.xlabels_top=False
    g1.ylabels_right=False
  
    #set title
    ax.set_title(title)
               
    #save path.  will either save as the title or a specified string
    if save_path != None and len(save_path) == 1:
        plt.savefig(save_path+"/"+title+".png")
    if save_path != None and len(save_path) == 2:
        plt.savefig(save_path[0]+"/"+save_path[1]+".png")

    plt.show()
    plt.clf()
""""""""""""""""""""""""""""""""""""""""""""""""""""""
###Below is a commented example of using the wrf_precipitation and plotting functions in conjunction
# from wrf_precip_plotting_functions import wrf_precipitation, plotting
# start_file_path = r"F:\MSD_2096_middle\wrfout_d01_2096-08-01_12%3A00%3A00.nc"
# total,lons,lats = wrf_precipitation(start_file_path,
#                                     lat_deg_ext = [30, 50],    ##bottom, top
#                                     lon_deg_ext = [-120, -80], ##left, right
#                                     )
# cont_tick = [0,2005,100]   ### often the contour and tick range are the same.  
# plotting(lons,lats,
#           total,
#           cont_tick,
#           cont_tick,
#           )

















    # Below was part of the wrf_precipitation function before I realized It was unnecessary and the three lines under each if statement could just be copied into the main function directly
    # #Given a latlon extent in degrees. will find the nearest index for creating subwindows of precipication
    # #This could probably be not in function form, but oh well.
    # def find_ids(start_file_path,lat_deg_ext=None,lon_deg_ext=None):
    #     """
    #     Given a file path,
    #     lat list [left edge, right edge], and
    #     lon list [bottom edge, top edge]
    #     Will find the nearest latlon index in a wrf 2d index array to use for creating sub windows of a larger wrfout file    
    #     """
    #     if lat_deg_ext != None:
    #         bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
    #         bottom_dist, top_dist = ((Dataset(start_file_path)['XLAT'][0,:,:]  - bottom_lat)**2)**0.5, ((Dataset(start_file_path)['XLAT'][0,:,:]  - top_lat)**2)**0.5   ###finds root error.  ((array - target value)squared)squareroot
    #         bottom_id,top_id = np.where(bottom_dist == bottom_dist.min())[0][0],np.where(top_dist == top_dist.min())[0][0]  ### [0][0] lats
    #     else:
    #         bottom_id,top_id=0,len(Dataset(start_file_path)['XLAT'][0,:,0])
        
    #     if lon_deg_ext != None:
    #         left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]
    #         left_dist, right_dist = ((Dataset(start_file_path)['XLONG'][0,:,:] - left_lon)**2)**0.5,   ((Dataset(start_file_path)['XLONG'][0,:,:] - right_lon)**2)**0.5
    #         left_id,right_id = np.where(left_dist == left_dist.min())[1][0],np.where(right_dist == right_dist.min())[1][0]  ### [1][0] lons
    #     else:
    #         left_id,right_id = 0,len(Dataset(start_file_path)['XLONG'][0,0,:])
    #     return(left_id,right_id,bottom_id,top_id)
    
    
    
    




""""""""""""""""""""""""""""""""""""""""""""""""""""""
"wrf precip and times per timestep. outputted as a list"
def prcp_timestep(file_path, start_time, start_timestep=0, end_timestep=None,lat_id_ext=None, lon_id_ext=None, lat_deg_ext=None, lon_deg_ext=None,):
    """
    file_path:      Required. The wrfout.nc to open
    start_time:     required. 6-item List.  [year, month, day, hour, minute, second] e.g., [2007,1,31,0,0,0]  requires datetime object and for the wrf time to be in minutes since this time
    start_timestep: The timestep index to be the starting point (to skip spinuptime)
    lat_id_ext:     Optional, if provided, indexes for creating only a specific latitude window.  otherwise it uses full matrix size
    lon_id_ext:     Optional, same as lat_id_ext but for longitude
    e.g., lat_id_ext=[93,134],lon_id_ext=[63,127] will make each variable change from (effectively) (timestep, :,:) to (timestep,93:134,63:127)
    lat_deg_ext:     Optional. Providing a degrees north latitude value, a sub-function finds the nearest latitude index/cell. e.g., lat_deg_ext=[bottom degree North, top degree North], or lat_deg_ext = [30.2735, 48.7]
    """
    #imports
    from netCDF4 import Dataset
    import numpy as np ##for the find_ids function below (.min())
    from datetime import datetime, timedelta
    
    
    #empty lists that willl contain arrays
    prcp_list = []
    date_list = []
    file = Dataset(file_path)
    
    
    #Set the end timestep or if unspecified, the end of the file.
    if end_timestep==None:
        end_timestep=len(file['XTIME'][:])
        
    #Set lat window if desired via index itself or finding the nearest index if given a lat degree
    if lat_id_ext != None:
        lat_id_ext = lat_id_ext
    elif lat_deg_ext != None:
        bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
        bottom_dist, top_dist = ((Dataset(file_path)['XLAT'][0,:,:]  - bottom_lat)**2)**0.5, ((Dataset(file_path)['XLAT'][0,:,:]  - top_lat)**2)**0.5   ###finds root error.  ((array - target value)squared)squareroot
        lat_id_ext = [np.where(bottom_dist == bottom_dist.min())[0][0],np.where(top_dist == top_dist.min())[0][0]]  ### [0][0] lats
    else:
        lat_id_ext=[0,len(Dataset(file_path)['XLAT'][0,:,0])]  
        
    #Set lon window the same way as the lat
    if lon_id_ext != None:
        lon_id_ext = lon_id_ext
    elif lon_deg_ext != None:
        left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]
        left_dist, right_dist = ((Dataset(file_path)['XLONG'][0,:,:] - left_lon)**2)**0.5,   ((Dataset(file_path)['XLONG'][0,:,:] - right_lon)**2)**0.5
        lon_id_ext = [np.where(left_dist == left_dist.min())[1][0],np.where(right_dist == right_dist.min())[1][0]]  ### [1][0] lons
    else:
        lon_id_ext=[0,len(Dataset(file_path)['XLONG'][0,0,:])]
    
    
    #Set the lat and lons that will be a deliverable
    lats = file['XLAT'][ 0,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
    lons = file['XLONG'][0,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
    
    
    #goes over each timestep and returns a list of arrays for precip
    for timestep in range(start_timestep+1,end_timestep):                                                     ###start_timestep+1 because we do current-previous. (e.g., timestep 24 is the actual start time, but we do timestep 25 as current and timestep 24 as prev)
        
        #We need the timestamps to know the change in timesteps.
        start_time = datetime(start_time[0], start_time[1], start_time[2], start_time[3], start_time[4], start_time[5])
        delta      = timedelta(minutes=int(file['XTIME'][timestep]))
        time       = start_time + delta
    
        #####"Collecting array of dbz and precip for the timestep"
        if 'I_RAINNC' in file.variables:
            curr_irain_nc = file['I_RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   # Buckets gridscale preicp (parameterization)
            curr_rain_nc  = file[  'RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #         gridscale precip (parameterization)
            curr_irain_c  = file[ 'I_RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   # Buckets convective precip (non-parameterization)
            curr_rain_c   = file[   'RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #         convective precip (non-parameterization)
            curr_nc_total = ((curr_irain_nc * 100) + curr_rain_nc)
            curr_c_total  = ((curr_irain_c  * 100) + curr_rain_c)
            curr_total    = curr_nc_total + curr_c_total
            
            
            prev_irain_nc = file['I_RAINNC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   
            prev_rain_nc  = file[  'RAINNC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_irain_c  = file[ 'I_RAINC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_rain_c   = file[   'RAINC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_nc_total = ((prev_irain_nc * 100) + prev_rain_nc)
            prev_c_total  = ((prev_irain_c  * 100) + prev_rain_c)
            prev_total    = prev_nc_total + prev_c_total

            total_prcp    = curr_total - prev_total
            
        else:
            curr_rain_nc  = file[  'RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            curr_rain_c   = file[   'RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            curr_total    = curr_rain_nc + curr_rain_c
            
            prev_rain_nc  = file[  'RAINNC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_rain_c   = file[   'RAINC'][timestep-1,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_total    = prev_rain_nc + prev_rain_c
            
            total_prcp    = curr_total - prev_total

        prcp_list.append(total_prcp)    
        date_list.append(time)
    file.close()
    return(date_list,prcp_list,lats,lons)
""""""""""""""""""""""""""""""""""""""""""""""""""""""





""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Unecessary now that the wrf_precipitation can handle an optional second file"
def wrf_precipitation_two_files(file_path_start,file_path_end,start_timestep=0):     ###This version means I don't have to manually do the I_rain values each time. It checks the file for it
    file_start = Dataset(file_path_start)
    file_end   = Dataset(file_path_end)
    lons,lats = file_start['XLONG'][0,:,:], file_start['XLAT'][0,:,:]
    if 'I_RAINNC' in file_start.variables:
        print("I_RAINNC is in the file")
        start_irain_nc = file_start['I_RAINNC'][start_timestep,:,:]   #Buckets non param precip
        start_rain_nc  = file_start[  'RAINNC'][start_timestep,:,:]   #non param precip
        start_irain_c  = file_start[ 'I_RAINC'][start_timestep,:,:]   #buckets param precip
        start_rain_c   = file_start[   'RAINC'][start_timestep,:,:]   # param precip
        start_nc_total = ((start_irain_nc * 100) + start_rain_nc)
        start_c_total  = ((start_irain_c * 100) + start_rain_c)
        start_total = start_nc_total + start_c_total
        
        end_irain_nc = file_end['I_RAINNC'][-1,:,:]
        end_rain_nc  = file_end[  'RAINNC'][-1,:,:]
        end_irain_c  = file_end[ 'I_RAINC'][-1,:,:]
        end_rain_c   = file_end[   'RAINC'][-1,:,:]
        end_nc_total = ((end_irain_nc * 100) + end_rain_nc)
        end_c_total  = ((end_irain_c * 100) + end_rain_c)
        end_total = end_nc_total + end_c_total
        
        total = end_total - start_total
        
    else: 
        start_rain_nc = file_start['RAINNC'][start_timestep,:,:]
        start_rain_c  = file_start[ 'RAINC'][start_timestep,:,:]
        start_total = start_rain_nc + start_rain_c
        
        end_rain_nc = file_end['RAINNC'][-1,:,:]
        end_rain_c  = file_end[ 'RAINC'][-1,:,:]
        end_total = end_rain_nc + end_rain_c
        
        total = end_total - start_total
        
    file_start.close()
    file_end.close()
    return(total,lons,lats)
""""""""""""""""""""""""""""""""""""""""""""""""""""""











""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Creating NC File"
def new_nc_wrf(new_file_path,
               lons,lats,
               new_file_title,
               new_var_name,
               new_var_std_name,
               var_to_write,
               ):
    from netCDF4 import Dataset
    import numpy as np
    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating File"
    new_file = Dataset(new_file_path,mode="w",format='NETCDF4')
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating Dimensions"
    y_dim = new_file.createDimension('y',184)  ###alter these to fityour data
    x_dim = new_file.createDimension('x',216)
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    new_file.title = new_file_title
    """"""""""""""""""""""""""""""""""""""""""""""""""

    """"""""""""""""""""""""""""""""""""""""""""""""""
    "Creating Variables"
    lat = new_file.createVariable('lat',np.float64,('y','x'))
    ###takes three arguments for create variable: name, type, and dimension. Not sure why theres's a comma after the dimension argument but following tutorial so...
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'

    lon = new_file.createVariable('lon',np.float64,('y','x'))### my assumption is this comma indicates there are no other dimensions associated with it
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



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def multiplot_x4(lons,lats,           ### lons and lats
                 plot_list,           ### list of plots to use.  will go [1,2], [3,4]
                 contour_range,       ### contour range
                 tick_range,          ### tick range should match contour range
                 cmap='viridis',      ### optional, colormap of choice
                 extent=None,         ### optional, [left, right, bottom, top]  in degrees latitude/longitude
                 suptitle="",         ### optional, if not set will be blank
                 subtitles=None,      ### optional, list of subtitles [1,2], [3,4]
                 save_path=None,      ### optional, provide directory to save to.  saves as supertitle.png
                 ):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import numpy as np
    
    
    contour_range = np.arange(contour_range[0],contour_range[1],contour_range[2])
    tick_range = np.arange(tick_range[0],tick_range[1],tick_range[2])
    
    ###Setting the general figure information
    fig,((ax1,ax2), (ax3,ax4)) = plt.subplots(2,2, 
                                              figsize=(11,6),
                                              subplot_kw={'projection':ccrs.PlateCarree()},
                                              gridspec_kw={'wspace':0.1},
                                              )
    fig.suptitle(suptitle)
    
    ###Setting each subplot's graphic
    """"""""""""""""""""""""""""""""""""""""""
    "Top Left"
    plot1 = ax1.contourf(lons, lats,
                         plot_list[0],
                         contour_range,
                         extend='max',
                         cmap = cmap,
                         )

    ax1.add_feature(cfeature.STATES,linewidth=0.6)                                                                                   ###creates teh outline of states
    g1 = ax1.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
    g1.xlabels_top=False
    g1.xlabels_bottom=False
    g1.ylabels_right=False
    """"""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""
    "Top Right"
    ax2.contourf(lons, lats,
                 plot_list[1],
                 contour_range,
                 cmap=cmap,
                 )
    ax2.add_feature(cfeature.STATES,linewidth=0.6)
    g2 = ax2.gridlines(draw_labels=False,linewidth=0.5,linestyle='--',alpha=1)
    """"""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""
    "Bottom Left"
    ax3.contourf(lons, lats,
                 plot_list[2],
                 contour_range,
                 cmap=cmap,
                 )
    ax3.add_feature(cfeature.STATES,linewidth=0.6)
    g3 = ax3.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
    g3.xlabels_top=False
    g3.ylabels_right=False
    """"""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""
    "Bottom Right"
    ax4.contourf(lons,lats,
                 plot_list[3],
                 contour_range,
                 cmap=cmap,
                 )
    ax4.add_feature(cfeature.STATES,linewidth=0.6)
    g4 = ax4.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
    g4.xlabels_top=False
    g4.ylabels_right=False
    g4.ylabels_left=False
    """"""""""""""""""""""""""""""""""""""""""
    
    ###Set extent or subtitles
    if extent != None:
        ax1.set_extent(extent)
        ax2.set_extent(extent)
        ax3.set_extent(extent)
        ax4.set_extent(extent)
    if subtitles != None:                                                                                                        ###Gotta set which plots show the lat lon values on the sides and bottom.  
        ax1.set_title(subtitles[0])
        ax2.set_title(subtitles[1])
        ax3.set_title(subtitles[2])
        ax4.set_title(subtitles[3])



    ###Set colorbar
    cax = fig.add_axes([0.91,0.15,0.04,0.7])                                                                                  ####cax within the colorbar is how you can define a new axis for the colorbar to stay on as opposed to the default trying to be under one of the subplots
    cbar = plt.colorbar(plot1,
                        orientation='vertical',
                        cax=cax,
                        ticks = tick_range,
                        pad = 0.05,
                        extend='max',
                        )
    
    ###Set Savepath
    if save_path != None:
        plt.savefig(save_path+"/"+suptitle+".png")
        
    plt.show()
    plt.clf()
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"This is likely to be used in conjunction with the 'prcp_timestep' function"
"Because 'prcp_timestep' finds the date_lsit for you necessary here."
def timestep_multiplot_x4(lons,lats,           ### lons and lats
                          plot_list,           ### list of plots to use.  will go [1,2], [3,4]
                          date_list,           ### list of dates
                          contour_range,       ### contour range
                          tick_range,          ### tick range should match contour range
                          cmap='viridis',      ### optional, colormap of choice
                          extent=None,         ### optional, [left, right, bottom, top]  in degrees latitude/longitude
                          suptitle="",         ### optional, if not set will be blank
                          subtitles=None,      ### optional, list of subtitles [1,2], [3,4]
                          save_path=None,      ### optional, provide directory to save to.  saves as supertitle.png
                          ):
    #imports
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import numpy as np
    
    contour_range = np.arange(contour_range[0],contour_range[1],contour_range[2])
    tick_range = np.arange(tick_range[0],tick_range[1],tick_range[2])
    
    for timestep in range(0,len(date_list)):
        ###Setting the general figure information
        fig,((ax1,ax2), (ax3,ax4)) = plt.subplots(2,2, 
                                                  figsize=(11,6),
                                                  subplot_kw={'projection':ccrs.PlateCarree()},
                                                  gridspec_kw={'wspace':0.1},
                                                  )
        fig.suptitle(str(date_list[timestep]) + "\n" + suptitle)
        
        ###Setting each subplot's graphic
        """"""""""""""""""""""""""""""""""""""""""
        "Top Left"
        plot1 = ax1.contourf(lons, lats,
                             plot_list[0][timestep][:,:],
                             contour_range,
                             extend='max',
                             cmap = cmap,
                             )
    
        ax1.add_feature(cfeature.STATES,linewidth=0.6)                                                                                   ###creates teh outline of states
        g1 = ax1.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
        g1.xlabels_top=False
        g1.xlabels_bottom=False
        g1.ylabels_right=False
        """"""""""""""""""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""
        "Top Right"
        ax2.contourf(lons, lats,
                     plot_list[1][timestep][:,:],
                     contour_range,
                     cmap=cmap,
                     )
        ax2.add_feature(cfeature.STATES,linewidth=0.6)
        g2 = ax2.gridlines(draw_labels=False,linewidth=0.5,linestyle='--',alpha=1)
        """"""""""""""""""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""
        "Bottom Left"
        ax3.contourf(lons, lats,
                     plot_list[2][timestep][:,:],
                     contour_range,
                     cmap=cmap,
                     )
        ax3.add_feature(cfeature.STATES,linewidth=0.6)
        g3 = ax3.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
        g3.xlabels_top=False
        g3.ylabels_right=False
        """"""""""""""""""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""""""""""""""
        "Bottom Right"
        ax4.contourf(lons,lats,
                     plot_list[3][timestep][:,:],
                     contour_range,
                     cmap=cmap,
                     )
        ax4.add_feature(cfeature.STATES,linewidth=0.6)
        g4 = ax4.gridlines(draw_labels=True,linewidth=0.5,linestyle='--',alpha=1)                                                   ###creates gridlines along lat lons
        g4.xlabels_top=False
        g4.ylabels_right=False
        g4.ylabels_left=False
        """"""""""""""""""""""""""""""""""""""""""
        
        ###Set extent or subtitles
        if extent != None:
            ax1.set_extent(extent)
            ax2.set_extent(extent)
            ax3.set_extent(extent)
            ax4.set_extent(extent)
        if subtitles != None:                                                                                                        ###Gotta set which plots show the lat lon values on the sides and bottom.  
            ax1.set_title(subtitles[0])
            ax2.set_title(subtitles[1])
            ax3.set_title(subtitles[2])
            ax4.set_title(subtitles[3])
    
    
    
        ###Set colorbar
        cax = fig.add_axes([0.91,0.15,0.04,0.7])                                                                                  ####cax within the colorbar is how you can define a new axis for the colorbar to stay on as opposed to the default trying to be under one of the subplots
        cbar = plt.colorbar(plot1,
                            orientation='vertical',
                            cax=cax,
                            ticks = tick_range,
                            pad = 0.05,
                            extend='max',
                            )
        
        ###Set Savepath
        if save_path != None:
            plt.savefig(save_path+"/"+str(date_list[timestep]).split(" ")[0] +"_"+str(date_list[timestep]).split(" ")[1][0:2] + "_" + str(date_list[timestep]).split(" ")[1][3:5] + ".png" )
            
        plt.show()
        plt.clf()
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Accumulating precip and dbz over a window and over a period"
"So for the current timestep we get the array for the spatial window size we want for dbz"
"Then for the same spatial window we subtract the previous timesteps precip from the current timestep's to get how much precip fell between last timestep and current"
"Then we use np.where to find how many cells are above a given threshold for dbz and precip"
def prcp_dbz_acc(file_path,start_timestep=0, prcp_thresh=1, dbz_thresh=10, lat_id_ext=None, lon_id_ext=None):
    #imports
    from netCDF4 import Dataset
    import numpy as np
    from datetime import datetime, timedelta

    ##Setting up tallys and lists to append tallys to.
    dbz_list = []
    prcp_list = []
    date_list = []
    file = Dataset(file_path)
    dbz_tally = 0
    prcp_tally = 0
    
    if lat_id_ext == None:
        lat_id_ext=[0,len(Dataset(file_path)['XLAT'][0,:,0])]                                                          ###if no input argument e.g., [93,134] it automatically goes from the index of 0 to the end
    if lon_id_ext == None:
        lon_id_ext=[0,len(Dataset(file_path)['XLONG'][0,0,:])]
    
    
    ###Iterating to get precip/dbz at each timestep
    for timestep in range(start_timestep+1,len(file['XTIME'][:])):            ###start_timestep+1 because we do current-previous. (e.g., timestep 24 is the actual start time, but we do timestep 25 as current and timestep 24 as prev)
        
        ###Get date for timestep for x-axis plotting
        start_time = datetime(2007, 7, 7, 0, 0, 0)                            ### simulation start time
        delta = timedelta(minutes=int(file['XTIME'][timestep]))               ### XTIME is minutes since simulation start 
        time = start_time + delta
    
        #####"Collecting array of dbz and precip for the timestep"
        dbz = file['COMDBZ'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]                          #gets the composite array dbz forthe current timestep and window
        if 'I_RAINNC' in file.variables:                                      #Universal wrf precip collection. if there is convection it'll grab these, if not it gets the other
            curr_irain_nc = file['I_RAINNC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]          #Buckets non param precip
            curr_rain_nc  = file[  'RAINNC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]          #non param precip
            curr_irain_c  = file[ 'I_RAINC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]          #buckets param preicp
            curr_rain_c   = file[   'RAINC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]          #param precip
            curr_nc_total = ((curr_irain_nc * 100) + curr_rain_nc)
            curr_c_total  = ((curr_irain_c  * 100) + curr_rain_c)
            curr_total    = curr_nc_total + curr_c_total
            
            prev_irain_nc = file['I_RAINNC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   
            prev_rain_nc  = file[  'RAINNC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_irain_c  = file[ 'I_RAINC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_rain_c   = file[   'RAINC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_nc_total = ((prev_irain_nc * 100) + prev_rain_nc)
            prev_c_total  = ((prev_irain_c  * 100) + prev_rain_c)
            prev_total    = prev_nc_total + prev_c_total

            total_prcp = curr_total - prev_total                              ###gets rainfall between current timestep and previous
            
        else:                                                                 ###If we're looking at sub parameter scale
            curr_rain_nc = file['RAINNC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            curr_rain_c  = file[ 'RAINC'][timestep,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            curr_total   = curr_rain_nc + curr_rain_c
            
            prev_rain_nc = file['RAINNC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_rain_c  = file[ 'RAINC'][timestep-1,lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
            prev_total   = prev_rain_nc + prev_rain_c
            
            total_prcp = curr_total - prev_total
 
    
 
        #### Tallying up each cell above the given threshold
        dbz_tally = dbz_tally + len(np.where(dbz >= dbz_thresh)[0])           ###adds number of cells >= threshold to the current tally
        prcp_tally = prcp_tally + len(np.where(total_prcp >= prcp_thresh)[0])
        dbz_list.append(dbz_tally)
        prcp_list.append(prcp_tally)                                          ### appending each timestep's tally so we can see how it grows    
        date_list.append(time)
    file.close()
    return(date_list,dbz_list,prcp_list)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def multi_file_prcp_timestep (dir_path,
                              start_time,
                              start_date=None, end_date=None, 
                              start_timestep=0,
                              lat_id_ext=None, lon_id_ext=None
                              ):
    import os
    from netCDF4 import Dataset
    from datetime import datetime, timedelta
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    #sortting function based on year, month, day, hour of wrf files
    def sortDates(datesList):
        split_up = datesList.split("-")
        ### wrfout_d03_2014-10-15_06%3A00%3A00.nc
        ###              0   1  2
        ### returns: [2014, 10, 15, 06]
        return   int(split_up[0][-4:]),  int(split_up[1]),  int(split_up[2][0:2]),      int(split_up[2][3:5])
    
    #implementation of sorting function
    files = os.listdir(dir_path)
    files = [file for file in files if file[3:6] == "out"]
    files.sort(key=sortDates)
    file_paths = [os.path.join(dir_path,sortedFileName) for sortedFileName in files]    ### list of sorted file paths
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    #Getting the start and end indices
    #finds where 2014-10-15_06 equals the same format of the full date list
    sliced_files = [item[11:24] for item in files]     
    if start_date != None:
        start_date = str(start_date[0])+"-"+str(start_date[1]).zfill(2) + "-" + str(start_date[2]).zfill(2) + "_"+ str(start_date[3]).zfill(2)
        start_id = [i for i,x in enumerate(sliced_files) if x==start_date][0]    ### np.where wasn't working but this works fine
    else:
        start_id = 0
        
    if end_date != None:
        end_date = str(end_date[0])+"-"+str(end_date[1]).zfill(2) + "-" + str(end_date[2]).zfill(2) + "_"+ str(end_date[3]).zfill(2)        
        end_id = [i for i,x in enumerate(sliced_files) if x==end_date][0]
        file_paths = file_paths[start_id:end_id+1]  ###sets the file_paths to go to whatever end date we want. but +1 because it stops one short of the provided id
        #print(file_paths)
    else:
        end_id = -1
        file_paths = file_paths[start_id:]     ###if we didn't specify the end_date this just goes over every file from starting point
        #print(file_paths)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
    #empty lists to append precip and dates
    prcp_list_temp = []
    
    date_list = []
    
    for path in file_paths:
        file = Dataset(path)


        if lat_id_ext == None:
            lat_id_ext=[0,len(file['XLAT'][0,:,0])]                                                          ###if no input argument e.g., [93,134] it automatically goes from the index of 0 to the end
        if lon_id_ext == None:
            lon_id_ext=[0,len(file['XLONG'][0,0,:])]
        
        end_timestep=len(file['XTIME'][:])
    

        lats = file[ 'XLAT'][0,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
        lons = file['XLONG'][0,  lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
    
        for timestep in range(start_timestep,end_timestep):                                                     ###start_timestep+1 because we do current-previous. (e.g., timestep 24 is the actual start time, but we do timestep 25 as current and timestep 24 as prev)
            #print(path,start_timestep,end_timestep,timestep)
            time_start = datetime(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
            delta      = timedelta(minutes=int(file['XTIME'][timestep]))
            time       = time_start + delta
        
            #####"Collecting array of dbz and precip for the timestep"
            if 'I_RAINNC' in file.variables:
                curr_irain_nc = file['I_RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #Buckets non param precip
                curr_rain_nc  = file[  'RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #non param precip
                curr_irain_c  = file[ 'I_RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #buckets param preicp
                curr_rain_c   = file[   'RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]   #param precip
                curr_nc_total = ((curr_irain_nc * 100) + curr_rain_nc)
                curr_c_total  = ((curr_irain_c  * 100) + curr_rain_c)
                curr_total    = curr_nc_total + curr_c_total
                total_prcp    = curr_total #- prev_total
                
            else:
                curr_rain_nc  = file[  'RAINNC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
                curr_rain_c   = file[   'RAINC'][timestep,    lat_id_ext[0]:lat_id_ext[1],  lon_id_ext[0]:lon_id_ext[1]]
                curr_total    = curr_rain_nc + curr_rain_c
                total_prcp    = curr_total #- prev_total
                
                
            if time not in date_list:
                prcp_list_temp.append(total_prcp)    
                date_list.append(time)
        file.close()
    
    
    prcp_list_final = [ curr-prev for curr,prev in zip(prcp_list_temp[1:],prcp_list_temp[:-1]) ]

    date_list = date_list[1:]
        
        
    return(date_list,prcp_list_final,lats,lons)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



from netCDF4 import Dataset
import numpy as np

def find_wrf_ids(start_file_path,lat_deg_ext,lon_deg_ext):
    """
    Given a file path,
    lat list [left edge, right edge], and
    lon list [bottom edge, top edge]
    Will find the nearest latlon index in a wrf 2d index array to use for creating sub windows of a larger wrfout file    
    """
    ### Define the edges desired by pulling from the provided inputs
    left_lon,right_lon = lon_deg_ext[0],lon_deg_ext[1]
    bottom_lat,top_lat = lat_deg_ext[0],lat_deg_ext[1]
    ### Creating distance arrays based on oprovided latlons in degrees.  can use absolute isntead of squares/squarerooots
    left_dist, right_dist = ((Dataset(start_file_path)['XLONG'][0,:,:] - left_lon)**2)**0.5,   ((Dataset(start_file_path)['XLONG'][0,:,:] - right_lon)**2)**0.5
    bottom_dist, top_dist = ((Dataset(start_file_path)['XLAT'][0,:,:]  - bottom_lat)**2)**0.5, ((Dataset(start_file_path)['XLAT'][0,:,:]  - top_lat)**2)**0.5
    ### Finding the indexes for the cell with the smallest distance from given latlons
    left_id,right_id = np.where(left_dist == left_dist.min())[1][0],np.where(right_dist == right_dist.min())[1][0]  ### [1][0] lons
    bottom_id,top_id = np.where(bottom_dist == bottom_dist.min())[0][0],np.where(top_dist == top_dist.min())[0][0]  ### [0][0] lats
    return(left_id,right_id,bottom_id,top_id)









    

# "Test"
# extent = [-93,-88.5,28.5,32.4]            ###NOLA        ##extent = [-91,-89,30,31.15]            ###NOLA zoom in
                                                            ###  long cells = 63:127    lat cells = 93: 134
# wrf_file_path = r"E:/nu-wrf_stuff/Outputs/NOLA_2007/final_outputs/Chem_Urban_NOLA/wrfout_d02_2007-07-07_00%3A00%3A00.nc"
# sim_precip = wrf_precipitation(wrf_file_path,24)[0]
# lons,lats = wrf_precipitation(wrf_file_path,24)[1],wrf_precipitation(wrf_file_path,24)[2]

# plotting(lons,lats,               ### set your lon lat values
#          sim_precip,              ### set your precip to be plotted
#          np.arange(0,61,2),       ### set your contour range, (min, max, scaling)
#          np.arange(0,61,2),       ### set your ticks, often this is the same as contour, but at a different scaling so the numbers to get jumbled
#          extent,                  ### set the visual box extent you want.  
#          "Chem Urban Precip",     #### set your title
#          )



"Getting a series ofwrf out files base on date range"
def wrf_daterange (path,start_date_str,end_date_str):
    """    
    path:                 String:         Required.  The path to the directory containing your wrf files.  Files are assumed to be in wrfout_d01_2013-01-01_00%3A00%3A00.nc format
    start_date_str:       String:         Required.  assumed to be in YYYY-MM-DD format
    end_date_str:         String:         Required.  Same as start_date_str format.  The function actually stops the day before the end date so if you set an end date of 2010-12-31, it would only pull files up to 2010-12-30
    
    Example wrf out: wrfout_d01_2013-01-01_00%3A00%3A00.nc
    Outputs a list of wrf filepaths based on a set date range.  It will not be in any reasonable order unfortunately.  You can blame os.lsitdir
    """
    
    import os
    from datetime import datetime
    
    #Setting up the input variables
    files = os.listdir(path)
    start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
    end_date = datetime.strptime(end_date_str,"%Y-%m-%d")
    
    #creating list of the files in the desired range.
    file_range = []
    for file in files:
        date_to_check_str = file.split("_")[2]                           ###wrfout_d01_2013-01-01_00%3A00%3A00.nc would be just the 2013-01-01 portion
        date_to_check = datetime.strptime(date_to_check_str,"%Y-%m-%d")  #converts string to datetime value
        if start_date <= date_to_check < end_date:                       #makes sure that it's the start date or beyond and then the day before the last date
            file_range.append(os.path.join(path,file))                   #appends the path with the file: p:/outputs/PR_dust_outputs/PR_dust_historic/PR_dust_historic_d01/outputs\\wrfout_d01_2014-12-24_06%3A00%3A00.nc
        else:
            pass                                                         #so if the file it's iterated over is not in the date range it does nothing    
    file_range.sort(key=lambda date: datetime.strptime(date.split("_")[2],"%Y-%m-%d"))  #sorts the dates into the proper order
    return(file_range)
#example
#path = r"p:/outputs/PR_dust_outputs/PR_dust_historic/PR_dust_historic_d01/outputs"
#start_date = "2013-12-31"
#end_date   = "2018-12-31"
#files = wrf_daterange(path,start_date,end_date)
#print(files)




"converting wrf XTIME into human readable"
def minutes_to_datetime(minutes_since_epoch,
                        epoch_start=[2013,1,1]
                        ):
    import datetime
    start = datetime.datetime(epoch_start[0],epoch_start[1],epoch_start[2])
    time_delta = datetime.timedelta(minutes=minutes_since_epoch)
    return(start+time_delta)
#test = minutes_to_datetime(2076840.) ##will be some time in 2016




"Finding the index for a given timestep within a file"
def find_time_idx(path,
                  epoch_start = [2013,1,1],
                  timestep = "00"
                  ):    
    """
    path          String         input path for a file.
    epoch_start   3-item list    e.g., [YYYY,M,D], [2013,6,31] the 'timesince...' part of the function. used in the sub-function
    timestep      String         2 item string.  This is the timestep you're looking for
    """    
    import datetime
    from netCDF4 import Dataset
    
    #sub function to get the conversion
    def minutes_to_datetime(minutes_since_epoch,
                            epoch_start
                            ):
        """
        minutes since epoch   interger     the outer function will automatically find these for you in XTIME
        epoch_start           3-item list  uses the list provided in the outerfunction so set it when making arguments for the outer function.
        """
        #import datetime
        start = datetime.datetime(epoch_start[0],epoch_start[1],epoch_start[2])
        time_delta = datetime.timedelta(minutes=minutes_since_epoch)
        return(start+time_delta)   ###returns a datetime object in the form of 2018-05-07 18:00:00  We will convert it to a string and then check the two digits for the hours (in this case 18Z)

    file = Dataset(path)
    for time in file['XTIME'][:]:
        if str(minutes_to_datetime(int(time),epoch_start)).split(" ")[1][0:2] == timestep:   #if the first two digits on the timesteps hour (00, 06, 12, 18) match your desired timestep it notes the index
            idx = np.where(file['XTIME'][:] == time)[0][0]
    file.close()
    return(idx)
#test_path = r"P:\outputs\PR_nodust_outputs\PR_historic_no_dust_files\PR_no_dust_historical_d01\wrfout_d01_2018-05-07_06%3A00%3A00.nc"
#index = find_time_idx(test_path)
#print(index)




