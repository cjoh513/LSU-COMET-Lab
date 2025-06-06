# Table of Contents
1. [Introduction](#introduction)
2. [Setting Up the "build-wrf" Directory](#setting-up-the-build-wrf-directory)
3. [System Environment Tests](#system-environment-tests)
   - [Conducting System Environment Tests](#conducting-system-environment-tests)
     - [Test 1](#test-1)
     - [Test 2](#test-2)
     - [Test 3](#test-3)
     - [Test 4](#test-4)
     - [Test 5](#test-5)
     - [Test 6](#test-6)
     - [Test 7](#test-7)  
4. [Building Libraries](#building-libraries)
   - [Export Variables](#export-variables)
   - [Install NetCDF-c](#install-netcdf-c)
   - [Exporting More Environmental Variables Post NetCDF-c](#exporting-more-environmental-variables-post-netcdf-c)
   - [Install NetCDF-Fortran](#install-netcdf-fortran)
   - [Install mpich](#install-mpich)
   - [Install zlib](#install-zlib)
   - [Install libpng](#install-libpng)
   - [Install jasper](#install-jasper)
   - [Install hdf5](#install-hdf5)
5. [Library Compatibility Test](#library-compatibility-test)
   - [Library Test 1](#library-test-1)
   - [Library Test 2](#library-test-2)
6. [Building WRF](#building-wrf)
   - [Configuring WRF](#configuring-wrf)
   - [Removing Leap Years from WRF](#removing-leap-years-from-wrf)
   - [Compiling WRF](#compiling-wrf)
7. [Building WPS](#building-wps)
   - [Configuring WPS](#configuring-wps)
   - [Removing Leap Years from WPS](#removing-leap-years-from-wps)
   - [Compiling WPS](#compiling-wps)
8. [Static Geography Data](#static-geography-data)
9. [Adding Environmental Variables to .bashrc](#adding-environmental-variables-to-bashrc)
&nbsp;


&nbsp;


# Introduction
This is a tuotrial for how to build and compile WPS and WRF on LSU's HPC systems.
It follows the official WRF tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php), but also includes photos and any tips or troubles I run into.  
&nbsp;

I am compiling this on a system that has all of the necessary libraries such as GNU gcc and Fortran already installed.  
&nbsp;

If something breaks or doesn't compile correctly, often times the best solution is to delete everything, restart your smic/linux terminal and start from scratch.  It is unfortunate, but starting over is often times faster than banging your head against the wall only for you to realize that the problem was you mistyped a variable name. 
&nbsp;

I highly recommend trying to go through the entire compilation process for both WRF and WPS in one go.  I don't recommend getting halfway through then stopping and coming back to it later.  It is very easy to lose track of which environmental variables you've exported. If you turn your computer off or restart the terminal, those variables will be reset and no longer exist (further explaination later).  Again, it can be annoying, but the best way to complete this tutorial is to do it all in one session.  It will probably take about 1-2 hours to complete depending on your linux aptitude.
&nbsp;

# Setting Up the "build-wrf" Directory
The first step is to prepare your tars and get your files in order.  We will make your build-wrf directory and download the necessary [WRF](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz)/[WPS](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz) tars
To get the WRF compilation tars for other versions of WRF, you can visit [THIS](https://github.com/wrf-model/WRF/releases) github.  
* Type:
  
```
cd /work/[your_username]
mkdir build-wrf
cd build-wrf
mkdir wrf_tars
cd wrf_tars
wget https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz
wget https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz
cd ..
```

# System Environment Tests
The Second step is to ensure your gfortran, cpp, and gcc are working.  
If you're compiling WRF on LSU's systems then these compilers should work without any issue as they are all preinstalled on the system.
If there is a version on the system then the below commands will identify the path to each.
* Type:
```
which gfortran 
which cpp  
which gcc
```
![image](https://github.com/user-attachments/assets/2e367f42-3a35-4da2-bc11-3726fdcc3f82).  

&nbsp;

* You should be within the "build-wrf" directory, you can type "pwd" to see which directory you're in.
* Now you will download the test files to ensure that Fortran and C are operating correctly.
* From your /work/[your_username]/build-wrf directory type:
```
mkdir tests
cd tests
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_tests.tar
tar -xf Fortran_C_tests.tar
``` 
![image](https://github.com/user-attachments/assets/1941f32d-4dd2-4af8-8f26-b7e9ae678f23)
I have a typo in the image above, I make the "/tests" directory in my "build-wrf/wrf_tars" directory.  Don't worry about that and just follow the instructions in the code blocks.

## Conducting System Environment Tests
* There are seven tests that will be run.  Each is a subheading below.
* From your "/work/[your_username]/build-wrf/tests" directory Type:
### Test 1
```
gfortran TEST_1_fortran_only_fixed.f
./a.out
```
* The following should be outputted: "SUCCESS test 1 fortran only fixed format".
### Test 2
```
gfortran TEST_2_fortran_only_free.f90
./a.out
```
* The following should be outputted: "Assume Fortran 2003: has FLUSH, ALLOCATABLE, derived type, and ISO C Binding
SUCCESS test 2 fortran only free format".  
### Test 3
```
gcc TEST_3_c_only.c
./a.out
```
* The Following should be outputted: "SUCCESS test 3 C only".
### Test 4
```
gcc -c -m64 TEST_4_fortran+c_c.c
gfortran -c -m64 TEST_4_fortran+c_f.f90
gfortran -m64 TEST_4_fortran+c_f.o TEST_4_fortran+c_c.o
./a.out
```
* The following should be outputted: "C function called by Fortran
Values are xx = 2.00 and ii = 1
SUCCESS test 4 fortran calling c".
### Test 5
In addition to the mentioned compilers the WRF build system relies on scripts as the user interface which rely on csh, perl, and sh.  
These tests ensure csh, perl, and sh are working properly.  
```
./TEST_csh.csh
```
* The following should be outputted: "SUCCESS csh test".
### Test 6
```
./TEST_perl.pl
```
* The following should be outputted: "SUCCESS perl test".
### Test 7
```
./TEST_sh.sh
cd ..
```
* The following should be outputted: "SUCCESS sh test".

&nbsp;

# Building Libraries  
Next, The libraries for GNU/gcc and WRF in general need to be built, but there are different ways people install these depending on specific environments and systems.  The [official](https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example-gnu.12385/) instructions do not work for me (There's something in the configure arguments that don't play nicely on LSU's systems), but following [MLandreau's](https://forum.mmm.ucar.edu/threads/ubuntu-20-04-configure-netcdf-fortran-4-5-2-error-c-compiler-cannot-create-executables.12707/) steps from the linked forum (9th entry down) consistently works.  This section will follow those steps for the library installation.  

These will also be specific versions of the libraries which may be outdated in the future.  If the versions used here do not work, you can check the forum tutorial linked above and UCAR's [files](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/) to find the most up-to-date libraries.  

&nbsp;
## Export Variables
* First you're going to set some variables that the compilation process expects.  Be warned, setting variables from the terminal in this manner does not save them.  When you close your smic/linux terminal, they will disappear and you will need to retype them.  They will be saved if added to your .bashrc file, but that will be handled at the end.
* Within your "/work/[your_username]/build-wrf" directory type:
```
mkdir libraries
cd libraries
DIR=[path-to-your-libraries]/libraries
export CC=gcc  
export CXX=g++  
export FC=gfortran  
export FCFLAGS=-m64  
export F77=gfortran  
export FFLAGS=-m64  
export JASPERLIB=$DIR/grib2/lib  
export JASPERINC=$DIR/grib2/include  
```
![image](https://github.com/user-attachments/assets/07902164-c181-49d8-820f-370fd3795ab7)  
I have a typo in the above image.  Instead of setting "F77=gfortran" I accidentally set "F77=-m64"

&nbsp;

## Install NetCDF-c
Within the "/work/[your_username]/build-wrf/libraries" directory, type:
```
wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz
tar xzvf v4.7.2.tar.gz
cd netcdf-c-4.7.2
./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared
```
The "./configure" command should end in a configuration summary looking something like this image  
![image](https://github.com/user-attachments/assets/f6e7a088-7842-45c2-a68f-a2acd661d666)
* Type:
```
make
make install
cd ..
rm v4.7.2.tar.gz
```  
After the "make install" command, if everything ran properly you should get a congratulations message like the image below.  
![image](https://github.com/user-attachments/assets/b611ab89-0de4-4536-ac08-2875ca45efa2)  
Within the "build-wrf/libraries" directory, there should now be the "netcdf" and "netcdf-c-4.7.2" files.  
![image](https://github.com/user-attachments/assets/b2fa377f-37b2-4b0e-9770-e4719fad8545)  





&nbsp;

## Exporting More Environmental Variables Post NetCDF-c
These are variables to set AFTER successfully installing NETCDF-C.  Setting these before you install NETCDF-C will cause the library install to break.  So if you need to restart the entire compilation process or reinstall NETCDF-C, be sure to remove the below variables or restart your smic/linux terminal so  these variables will no longer be set.
* Type:
```
export PATH=$DIR/netcdf/bin:$PATH  
export NETCDF=$DIR/netcdf  
export LIBS="-lnetcdf"  
export LDFLAGS=-L$DIR/netcdf/lib  
export CPPFLAGS=-I$DIR/netcdf/include
```
![image](https://github.com/user-attachments/assets/9fd28784-115a-483a-9f46-9f2e412053e1)

&nbsp;

## Install NetCDF-Fortran
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz
tar xzvf v4.5.2.tar.gz
cd netcdf-fortran-4.5.2
./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared
make
make install  
cd ..  
rm v4.5.2.tar.gz
```
![image](https://github.com/user-attachments/assets/5a53abf6-f111-46cd-a101-0075d8d1fbab)  


&nbsp;

## Install mpich
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/mpich-3.0.4.tar.gz  
tar xzvf mpich-3.0.4.tar.gz
cd mpich-3.0.4
./configure --prefix=$DIR/mpich
make
make install
cd ..
rm mpich-3.0.4.tar.gz  
export PATH=$DIR/mpich/bin:$PATH
```

&nbsp;

## Install zlib
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz
tar xzvf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=$DIR/grib2
make
make install
cd ..
rm zlib-1.2.11.tar.gz
export LDFLAGS="-L$DIR/grib2/lib -L$DIR/netcdf/lib"
export CPPFLAGS="-I$DIR/grib2/include -I$DIR/netcdf/lib"
```
![image](https://github.com/user-attachments/assets/ada181cd-b96e-498e-9ad0-c2b472d0979e)  

&nbsp;


## Install libpng
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
tar xzvf libpng-1.2.50.tar.gz
cd libpng-1.2.50
./configure --prefix=$DIR/grib2
make
make install
cd ..
rm libpng-1.2.50.tar.gz
```

&nbsp;


## Install jasper  
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz
tar xzvf jasper-1.900.1.tar.gz
cd jasper-1.900.1
./configure --prefix=$DIR/grib2
make
make install
cd ..
rm jasper-1.900.1.tar.gz
```

&nbsp;

## Install hdf5
* From the "/work/[your_username]/build-wrf/libraries" directory type:
```
wget https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_5.tar.gz
tar xzvf hdf5-1.10.5.tar.gz
cd hdf5-hdf5-1_10_5
./configure --prefix=$DIR/netcdf --with-zlib=$DIR/grib2 --enable-fortran --enable-shared
make
make install
cd ..
rm hdf5-1.10.5.tar.gz
cd ../tests
```

&nbsp;


# Library Compatibility Test
You've ensured the compilers are compatible, but now we need to ensure that the libraries of Fortran, C, and NetCDF are compatible.    
* From the "/work/[your_username]/build-wrf/tests" directory type:
```
wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_NETCDF_MPI_tests.tar
```

## Library Test 1
* Type:
```
cp ${NETCDF}/include/netcdf.inc .
gfortran -c 01_fortran+c+netcdf_f.f
gcc -c 01_fortran+c+netcdf_c.c
gfortran 01_fortran+c+netcdf_f.o 01_fortran+c+netcdf_c.o \-L${NETCDF}/lib -lnetcdff -lnetcdf
./a.out
```
* The following should be outputted:
  * "C function called by Fortran
  * Values are xx = 2.00 and ii = 1
  * SUCCESS test 1 fortran + c + netcdf"
## Library Test 2
* Type:
```
mpif90 -c 02_fortran+c+netcdf+mpi_f.f
mpicc -c 02_fortran+c+netcdf+mpi_c.c
mpif90 02_fortran+c+netcdf+mpi_f.o \
02_fortran+c+netcdf+mpi_c.o \
     -L${NETCDF}/lib -lnetcdff -lnetcdf
mpirun ./a.out
cd ..
```
* The following should be outputted:
  * C function called by Fortran
  * Values are xx = 2.00 and ii = 1
  * status = 2
  * SUCCESS test 2 fortran + c + netcdf + mpi  


 &nbsp;  

# Building WRF
Now we can actually compile WRF and then WPS.  For this tutorial and in general, I use version [WRF-4.2.2](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz).  The configuration choices will be chosen with LSU's systems in mind.  
## Configuring WRF
* From the "/work/[your_username]/build-wrf/" directory type:
```
wget https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz
tar xzvf v4.2.2.tar.gz
rm v4.2.2.tar.gz
```
This should create a directory called "WRF-4.2.2"  
![image](https://github.com/user-attachments/assets/11a29fcb-dde3-4c37-905a-378849997422)  
 
Now we'll configure before compiling.  
* From the "/work/[your_username]/build-wrf/" directory type:
```
cd WRF-4.2.2
./configure
```
* You'll see a large number of options for you to select how to configure WRF based on your system.
* They correspond to which compiler you are using and whether you want WRF to run serially, Shared-Memory Parallelism, or with Distributed-Memory Parallelism.  More information on these can be found [here](https://forum.mmm.ucar.edu/threads/compiling-options-serial-vs-smpar-vs-dmpar.65/).  
    * Because LSU's systems use a series of clusters and we compiled with gfortran select option 34 by typing "34"
    * type "1" for the "Compile for nesting?" option.  This allows nested simulations.
    * ![image](https://github.com/user-attachments/assets/6ac672f6-c70b-44ab-9d73-add55803f8ed)  

## Removing Leap Years from WRF
If you wish to compile your WRF without Leap Days (i.e., skips Feb. 29th every 4 years), follow these steps.  If you want leap-days then you can skip to the "Compiling WRF" step
* From the "/work/[your_username]/build-wrf/WRF-4.2.2" directory open the "configure.wrf" file.
* Navigate down to the "Architecture Specific Settings" section.
* To the line "ARCH_LOCAL" add at the end, "-DNO_LEAP_CALENDAR"
* Save and close "configure.wrf"
![image](https://github.com/user-attachments/assets/9ddbde93-1be7-490c-9338-e98fb80f2e42)


&nbsp;



&nbsp;

## Compiling WRF
Now that you've configured WRF either with or without leap days pick back up here!
* From the "/work/[your_username]/build-wrf/WRF-4.2.2" directory type:
```
./compile em_real >& log.compile
```
* The process will probably take some time (maybe 20-30 minutes).
* This tutorial uses the "em_real" "case_name", which is the most common option and what I use as it's designed for real data situations.  Other options can be found in the official WRF tutorial [here](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php).
* The end of the log.compile should look like the picture below if it ran correctly.  
![image](https://github.com/user-attachments/assets/3eb0f3c2-573d-4a00-8d1c-f628e1f92fa6)  
You can also check that the essential .exe files were properly created by typing:
```
ls -ls main/*.exe
cd ..
```
![image](https://github.com/user-attachments/assets/5c651dc0-ea90-49d8-8c58-2f31f6dd97b7)  
The numbers circled are the file size in bytes.  If they are 0 bytes, something has gone wrong in the compilation process and you need to check the log.compile for an error.  
Congrats! You've successfully compiled WRF-4.2.2 and now we only need to worry about WPS.  





&nbsp;
# Building WPS
Now that WRF is built, we can build WPS.  I will be using [WPS-4.2](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz) which is compatible with WRF-4.2.2.  WPS configuration choices will be chosen with LSU's systems in mind.
## Configuring WPS
This step will build the WRF-Preprocessing System.  It will be very similar to the Building WRF section.  
First, download and extract the WPS directory.  
* From the "/work/[your_username]/build-wrf" directory type:
```
wget https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz  
tar xzvf v4.2.tar.gz
rm v4.2.tar.gz
cd WPS-4.2
```
![image](https://github.com/user-attachments/assets/e18e3f4c-68a4-4111-8c94-88be92547b0c)

&nbsp;

* From the "/work/[your_username]/build-wrf/WPS-4.2" directory type:
```
export WRF_DIR=/work/[your_username]/build-wrf/WRF-4.2.2
./configure
```
*  There will be 40 options for compilers to use for WPS.  We want to compile WPS with the same compiler chosen in the Building WRF step.  For myself—because we used gfortran, want the ability to use clusters on LSU systems, and nest simulations—we are choosing the "Linux x86_64, gfortran (dmpar)" option.
![image](https://github.com/user-attachments/assets/9eac0e28-2819-4265-9b9b-3637e58b857f)

## Removing Leap Years from WPS
Similar to WRF, if you're running a similation with a Feb. 29th but your forcing data doesn't account for leap days, WPS will fail to run.  This step tells you how you can prevent WPS from incorporating Feb. 29th.  This step is not necessary and you can skip to the "Compiling WPS" section below.
* After configuring WPS, a "configure.wps" file will be created.
  * Open the "configure.wps"
  * Navigate to the subheading "Architecture Specific Settings" and find the line "CPPFLAGS"
  * At the end of that line, add "-DNO_LEAP_CALENDAR"
  * Save and Close
  * ![image](https://github.com/user-attachments/assets/18a04931-2ad4-4700-ac54-e9a305f7abe7)

 &nbsp;



 &nbsp;


 &nbsp;

## Compiling WPS
 If you completed or skipped the "Removing Leap Years from WPS" section, pick back up here with the compilation!
* From the "/work/[your_username]/build-wrf/WPS-4.2" directory type:
```
./compile >& log.compile
```
![image](https://github.com/user-attachments/assets/bd74ef03-0ea1-45b2-bc4c-016da6b32421)
 * This will only take a couple minutes to finish.  Once done, 3 executables should appear in the WPS-4.2 directory
   * geogrid.exe
   * ungrib.exe
   * metgrid.exe   
 * The .exe files listed above are symbolic links.  A symbolic link is kind of like a desktop shortcut.  The file itself is not housed in the top-level of the WPS directory, but we've created a shortcut and can manipulate each of those files for ease.
 * To ensure the WPS process ran correctly, make sure each of these is not zero sized by typing the following from the "/work/[your_username]/build-wrf/WPS-4.2" directory:
```
ls -ls geogrid/src/geogrid.exe
ls -ls metgrid/src/metgrid.exe
ls -ls ungrib/src/ungrib.exe
cd ..
```
![image](https://github.com/user-attachments/assets/b4243502-5cf8-4b0c-9de7-12ef2099c3bc)  

   &nbsp;

   &nbsp;

   &nbsp;

# Static Geography Data
The hard parts are done, now you just need the "static geography data."  These are variables such as soiltype or albedo or land useage that does not change often and so is considered "static" data necessary for WRF to run.  
The link to the download page is [HERE](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html). 

&nbsp;

Important Note: In my experience, geogrid.exe often requires a few more geog files than are actually provided in the tar.  If you encounter an error running geogrid.exe related to a non-existing file in the geog directory, go to the above webpage and manually download and add it to the geog directory.  There is also a step-by-step guide on how to do this on the "Troubleshooting and Tips.md" page of this github.  

&nbsp;

Navigate to your "/work/[your_username]/build-wrf/" directory and type:
```
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
tar -xf geog_high_res_mandatory.tar.gz
```
* Important Note: this will be about 30GB of data
* When you use the WPS process, in the namelist.wps be sure to set the "geog_data_path" to this directory with:
  *  geog_data_path = /work/[your_username]/build-wrf/[geog_directory_name]
  *  ("WPS_GEOG" is a newer and common geog directory naming convention, mine is called "geog" in the picture below)
  ![image](https://github.com/user-attachments/assets/24feb2d9-2384-468d-8aa1-2f8a5650ed36)
 

&nbsp;

# Adding Environmental Variables to .bashrc
This section takes most of those environmental variables set at the start of the tutorial and adds them to your .bashrc file.  This is important because otherwise when you close the terminal you'll lose the environmental variables you set, some of which are essential to run WRF.  

*Open the .bashrc file with either of the below commands:
```
vi ~/.bashrc
```
or
```
nano ~/.bashrc
```
*  Make sure the below environmental variables  are added to your .bashrc
```
export WRF_DIR=/work/cjoh513/build-wrf/WRF-4.2.2
export WRF_CHEM=1
export WRF_KPP=0
export WRFIO_NCD_LARGE_FILE_SUPPORT=1
export DIR=/work/cjoh513/build-wrf/libraries
export PATH=$DIR/netcdf/bin:$DIR/mpich/bin:$PATH
export NETCDF=$DIR/netcdf
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS=-m64
export F77=gfortran
export FFLAGS=-m64
```
* Here is an example of what mine looks like, but there are a few more variables added than strictly for this tutorial.  
![image](https://github.com/user-attachments/assets/472643fb-5907-4670-934e-331637da16e7)  




Congratulations!!!  
The process may have been arduous, but you've successfully installed libraries and compiled WRF/WPS.  





  






