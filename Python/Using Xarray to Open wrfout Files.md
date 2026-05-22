# Introduction
This is a tutorial for how to incorporate Xarray into your wrfout data analysis.  
Xarray is a powerful Python package designed to build upon NumPy and Pandas, ingesting and interacting with multi-dimensional arrays.
For example, WRF output variables are often these multi-dimensional arrays possibly encompassing time, latitude, longitude, height, and depth.  
Often, wrfout files contain only a few timesteps per day but encompass full years.  Xarray offers the ability to bulk open and organize your data with ease.

# Installation
Anaconda is recommended as the easiest way to install Xarray and the necessary dependencies.  
This tutorial uses python version 3.12.  
You can install the packages manually or use the Environment YAML file to install them for you.  
Using Anaconda Prompt create a new environment and install the core packages.
```
conda create -n wrf-xarray python=3.11
conda activate wrf-xarray
conda install -c conda-forge xarray dask netcdf4 h5netcdf
```
* This installs:  
xarray → labeled array analysis  
dask → lazy parallel computation (for large datasets)
netcdf4 → NetCDF backend  
h5netcdf → alternate backend

## Additional Recommended Installations  
Below are additional commonly installed and recommeneded python packages related to using wrfout data.  
These all pair nicely with Xarray and are almost essential for geospatial data manipulation.
Using Anaconda Prompt:
```
conda install -c conda-forge wrf-python numpy pandas matplotlib cartopy
```
* This installs:  
numpy → numerical operations  
pandas → time handling  
matplotlib → plotting  
cartopy → maps/projections  

## Verify Installation
Recommend opening up python and importing the packages to ensure no errors arise.
```
import xarray as xr
import dask
import netCDF4
import wrf

print(xr.__version__)
```

## Alternate Installation
You can use the Evironment YAML (wrf-xarray-environment.yml) file to create the environment and install the necessary packages too.
```
conda env create-f wrf-xarray-environment.yml
conda activate wrf-xarray
```

Unfinished. Next steps are to discuss Datasets and DataArrays then how to open files
