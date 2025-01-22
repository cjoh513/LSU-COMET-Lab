# Introduction
This is a written account of my attempt to compile WRF4.2 as of 1/22/2025.  
This follows the official WRF tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php), but also includes photos and any tips or troubles I run into.  
Important Note: I am compiling this on a system that has all of the necessary libraries such as GNU gcc and foretran already installed.  

# Tars
The first step is to prepare your tars and get your files in order.  
To get the WRF compilation tar, you can visit [THIS](https://github.com/wrf-model/WRF/releases) github.  
* Make a new directory called "build-wrf".
* "cd" into the "build-wrf" directory and make a new directory called "wrf_tars".
* "cd" into "build-wrf/wrf_tars" and download the [WRF](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz) and [WPS](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz) tars using "wget"




