# Introduction
This is a written account of my attempt to compile WRF4.2 as of 1/22/2025.  
This follows the official WRF tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php), but also includes photos and any tips or troubles I run into.  
&nbsp;

Important Note: I am compiling this on a system that has all of the necessary libraries such as GNU gcc and foretran already installed.  
&nbsp;

Important Note: The items I tell you to type are in quotes. Don't type the quotes.  They are simply there to help delineate instructions.
For example, if I tell you to type "which gfortran", you type what's between the quotes but not the quotes themselves.  

# Tars
The first step is to prepare your tars and get your files in order.  
To get the WRF compilation tar, you can visit [THIS](https://github.com/wrf-model/WRF/releases) github.  
* Make a new directory called "build-wrf".
* "cd" into the "build-wrf" directory and make a new directory called "wrf_tars".
* "cd" into "build-wrf/wrf_tars" and download the [WRF](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz) and [WPS](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz) tars using "wget".
![image](https://github.com/user-attachments/assets/065b83a3-8a58-4bf6-bc40-fa77cef199f8).


# System Environment Tests
The Second step is to makesure your gfortran, cpp, and gcc are working.  
If you're compiling WRF on LSU's systems then these compilers should work without any issue as they are all preinstalled on the system.
* type "which gfortran".  
* type "which cpp".  
* type "which gcc".  
If there is a version on the system then the above commands will identify the path to each.
![image](https://github.com/user-attachments/assets/2e367f42-3a35-4da2-bc11-3726fdcc3f82).  

&nbsp;

* Within the "build_wrf" directory, create a new directory called "tests".
* "cd" into the new "tests" directory.
* use "wget" to download the Fortran and C Tests from [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_tests.tar).  
![image](https://github.com/user-attachments/assets/1941f32d-4dd2-4af8-8f26-b7e9ae678f23).
* Unpack the tar file with "tar -xf Fortran_C_tests.tar".
There are Seven tests that will be run.  Each is a subheading below.  
### Test #1
* Type "gfortran TEST_1_fortran_only_fixed.f".
* Type "./a.out".
* The following should be outputted: "SUCCESS test 1 fortran only fixed format".
### Test #2
* Type "gfortran TEST_2_fortran_only_free.f90".
* Type "./a.out".
* The following should be outputted: "Assume Fortran 2003: has FLUSH, ALLOCATABLE, derived type, and ISO C Binding
SUCCESS test 2 fortran only free format".  
### Test #3
* Type "gcc TEST_3_c_only.c".
* Type "./a.out".
* The Following should be outputted: "SUCCESS test 3 C only".
### Test #4
* Type "gcc -c -m64 TEST_4_fortran+c_c.c".
* Type "gfortran -c -m64 TEST_4_fortran+c_f.f90".
* Type "gfortran -m64 TEST_4_fortran+c_f.o TEST_4_fortran+c_c.o".
* Type "./a.out".
* The following should be outputted: "C function called by Fortran
Values are xx = 2.00 and ii = 1
SUCCESS test 4 fortran calling c".
### Test #5
In addition to the mentioned compilers the WRF build system relies on scripts as the user interface which rely on csh, perl, and sh.  
These tests ensure csh, perl, and sh are working properly.  
* Type "./TEST_csh.csh".
* The following should be outputted: "SUCCESS csh test".
### Test #6
* Type "./TEST_perl.pl".
* The following should be outputted: "SUCCESS perl test".
### Test #7
* Type "./TEST_sh.sh".
* The following should be outputted: "SUCCESS sh test".

&nbsp;

# Building Libraries  
Next, The libraries for GNU/gcc need to be built.  The online tutorial at the top of this file will link you to the WRF-Forums for installation instructions.  
[THIS](https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example-gnu.12385/) also links directly to the forum installation instructions as well.  
The commands within this tutorial will be for specific versions of the libraries which may be outdated in the future.  If the versions used here do not work, you can check the forum tutorial linked above and UCAR's [files](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/) to find the most up-to-date libraries.  

&nbsp;

* Within the "build-wrf" directory make a new directory with the command "mkdir libraries"  
This is the directory where the essential WRF libraries will be installed.

* Type the below set of commands on individual lines to set environment variables.  Be warned, until we add them to the .bashrc file, they will be cleared if you close the terminal.  I won't be enclosing them in quotes because some of the commands have quotes within the command itself, but I do have a photo showing each as well.
* DIR=[path-to-your-libraries]/libraries
* export NETCDF=$DIR/netcdf
* export LD_LIBRARY_PATH=$NETCDF/lib:$DIR/grib2/lib
* export PATH=$NETCDF/bin:$DIR/mpich/bin:${PATH}
* export JASPERLIB=$DIR/grib2/lib
* export JASPERINC=$DIR/grib2/include
* export CC=gcc
* export CXX=g++
* export FC=gfortran
* export FCFLAGS="-m64 -fallow-argument-mismatch"
* export F77=gfortran
* export FFLAGS="-m64 -fallow-argument-mismatch"
* export LDFLAGS="-L$NETCDF/lib -L$DIR/grib2/lib"
* export CPPFLAGS="-I$NETCDF/include -I$DIR/grib2/include -fcommon"
![image](https://github.com/user-attachments/assets/accb164c-a19f-41d1-bb86-94aeb64244a4)

### Install zlib
* "cd" into the "build-wrf/libraries" directory
* Type the following commands:
* wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz
* tar xzvf zlib-1.2.11.tar.gz
* cd zlib-1.2.11
* ./configure --prefix=$DIR/grib2
* make -j 4
* make install
* cd ..
* rm -rf zlib*  
You should be left with a directory "grib2" in the "libraries" directory  
![image](https://github.com/user-attachments/assets/12a2aa61-8fa2-4a17-b87c-76d62db93201)

### Install HDF5
* within the "build-wrf/libraries" directory type the following commands:
* wget https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_5.tar.gz
* tar xzvf hdf5-1_10_5.tar.gz
* cd hdf5-hdf5-1_10_5/
* 

&nbsp;

# Library Compatibility Test
We've ensured the compilers are compatible, but now we need to ensure that the libraries of Fortran, C, and NetCDF are compatible.  
Again, if you're compiling these on LSU's systems there should be no incompatiblities.  
* In the same "build_wrf/tests" directory, download [THIS](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_NETCDF_MPI_tests.tar) tar file which contains the libraries test files.
* Unpack the tar file with "tar -xf Fortran_C_NETCDF_MPI_tests.tar"
### Test #1
* 








