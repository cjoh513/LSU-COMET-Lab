# Introduction
This is a tutorial for how to incorporate Xarray into your wrfout data analysis, much of the information is taken from the [Xarray documentation](https://docs.xarray.dev/en/stable/getting-started-guide/index.html).  

Xarray is a powerful Python package designed to build upon NumPy and Pandas, ingesting and interacting with multi-dimensional arrays.  

For example, WRF output variables are often multi-dimensional arrays encompassing time, latitude, longitude, height, and depth.  
Often, wrf simulations span multiple years split into only a few timesteps per out-file per day.  Xarray offers the ability to bulk open and organize your data with ease.

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
conda env create -f wrf-xarray-environment.yml
conda activate wrf-xarray
```
# Basic Information and Data Structures
Arrays found in files like wrfouts typically have "labels." These encode information about how the array values are mapped to geospatial coordinates, or time, or verticality.  If you just extract an array from wrfout using basic techniques, you extract none of the label information. You simply have an array of numbers. 

For example, 2-meter Temperature in wrfout has Time, south_north, and east_west dimensions.  A common way to retrieve 2-meter temperature for the first timestep would be "file["T2"][0,:,:]".  The variable returned would be a 2D array with no information regarding those dimension labels (Time, south_north, and east_west)

This can be perfectly fine, but when you need to extract a specific day or latitude/longitude range, it requires you to get creative in your approach to retrieve that data (usually through complicated indexing methods).  

Xarray data structures keep the array labels which allow you to more easily and concisely extract specific data, dates, regions, groupings and alignments.  Additionally, because the package uses labels, it means that you can more easily interpret your code.

## Data Structures
The two important datas strucutres are designed to bolster NumPy and Pandas arrays.
* DataArray: The labeled N-dimensional array.  For example, a specific variable like LAI, T2, or QCLOUD within a wrfout file.
* Dataset: The dictionary-like container of multiple DataArrays.  This is the wrfout file itself.  
So when you use Xarray to open a wrfout file, you are opening a Dataset and then can extract specific DataArrays by calling for the variables of interest.

# Opening and Viewing Datasets and DataArrays
Once installed and you've ensured that you can import the necessary packages, it's time to get started.  

The first step is practice opening and understanding the wrfout file.
## Opening A Single File
The basic function to open a file is [xarray.open_dataset](https://docs.xarray.dev/en/stable/generated/xarray.open_dataset.html). This function loads in a single file as the Dataset structure.
```
import xarray as xr
path = [path\to\wrfout\file]
ds = xr.open_dataset(path)
print(ds)
```
The below example is what the code block would print from a wrfout file examining at June 1, 2014 over a rectangular domain across the Atlantic ocean.  
<img width="1276" height="1204" alt="image" src="https://github.com/user-attachments/assets/342ef32d-12d7-4c70-acaa-11dc36dc92e7" />
The Dataset contains dimension labels, coordinate labels, and individual DataArrays in the form of the "Data Variables" listed.
## Using Variables
Now, the entire wrfout file is open, but the variable DataArrays within are more important.  These are easily callable through labelling.  Each wrfout variable's label is the variable name.  For example, 2-meter temperature is "T2" and Sea Surface Temperature is "SST". Below, is an example calling the 2-meter temperature DataArray.
```
t2 = ds.T2
print(t2)
```
I'm now pivoting to finishing this tutorial through an jupyter lab notebook that will get uploaded here.
