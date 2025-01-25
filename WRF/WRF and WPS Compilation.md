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
Next, The libraries for GNU/gcc need to be built.  There are different ways people install the necessary libraries for WRF.  The [official](https://forum.mmm.ucar.edu/threads/full-wrf-and-wps-installation-example-gnu.12385/) instructions do not work for me (There's something in the configure arguments that don't play nicely on LSU's systems), but following [MLandreau's](https://forum.mmm.ucar.edu/threads/ubuntu-20-04-configure-netcdf-fortran-4-5-2-error-c-compiler-cannot-create-executables.12707/) steps from the linked forum (9th entry down) consistently works.  This section will follow those steps for the library installation.  

The commands within this tutorial will be for specific versions of the libraries which may be outdated in the future.  If the versions used here do not work, you can check the forum tutorial linked above and UCAR's [files](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/) to find the most up-to-date libraries.  

&nbsp;

* Within the "build-wrf" directory make a new directory with the command "mkdir libraries"  
This is the directory where the essential WRF libraries will be installed.

* Type the below set of commands on individual lines to set environment variables.  Be warned, until we add them to the .bashrc file, they will be cleared if you close the terminal.  I won't be enclosing them in quotes because some of the commands have quotes within the command itself, but I do have a photo showing each as well.
* If interested, these are setting variables that will come up for much of the compilation process
* DIR=[path-to-your-libraries]/libraries
* export CC=gcc  
* export CXX=g++  
* export FC=gfortran  
* export FCFLAGS=-m64  
* export F77=gfortran  
* export FFLAGS=-m64  
* export JASPERLIB=$DIR/grib2/lib  
* export JASPERINC=$DIR/grib2/include  
![image](https://github.com/user-attachments/assets/07902164-c181-49d8-820f-370fd3795ab7)

&nbsp;

### Install NetCDF-c
Within the "build-wrf/libraries" directory, type the below set of commands:
* wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz
* tar xzvf v4.7.2.tar.gz
* cd netcdf-c-4.7.2
* ./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared  
Important Note: the "./configure" command should end in a configuration summary looking something like this image  
![image](https://github.com/user-attachments/assets/f6e7a088-7842-45c2-a68f-a2acd661d666)
* type the following commands
* make
* make install  
Important Note: After the "make install" command, if everything ran properly you should get a congratulations message like the image below.  
![image](https://github.com/user-attachments/assets/b611ab89-0de4-4536-ac08-2875ca45efa2)  
Within the "build-wrf/libraries" directory, there should now be the "netcdf", "netcdf-c-4.7.2", and "v4.7.2.tar.gz" files.  
![image](https://github.com/user-attachments/assets/b2fa377f-37b2-4b0e-9770-e4719fad8545)  
Clean up by removing the .tar file with the command "rm v4.7.2.tar.gz".  You may want to wait until the end to remove this in case you run into hiccups and need a fresh copy from the .tar file.  
![image](https://github.com/user-attachments/assets/7f82446f-db78-410c-aba6-07641d59c4c4)  




&nbsp;

### Setting More Environmental Variables
Set a few more environmental variables by putting the following commands:  
* export PATH=$DIR/netcdf/bin:$PATH  
* export NETCDF=$DIR/netcdf  
* export LIBS="-lnetcdf"  
* export LDFLAGS=-L$DIR/netcdf/lib  
* export CPPFLAGS=-I$DIR/netcdf/include  
![image](https://github.com/user-attachments/assets/9fd28784-115a-483a-9f46-9f2e412053e1)

&nbsp;

### Installing netcdf-fortran
type the following commands:
* wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz
* tar xzvf v4.5.2.tar.gz
* cd netcdf-fortran-4.5.2
* ./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared
* make
* make install  
* cd ..  
* rm v4.5.2.tar.gz
![image](https://github.com/user-attachments/assets/5a53abf6-f111-46cd-a101-0075d8d1fbab)  


&nbsp;

### Installing mpich
type the following commands:
* wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/mpich-3.0.4.tar.gz  
* tar xzvf mpich-3.0.4.tar.gz
* cd mpich-3.0.4
* ./configure --prefix=$DIR/mpich
* make
* make install
* cd ..
* rm mpich-3.0.4.tar.gz  
* export PATH=$DIR/mpich/bin:$PATH

&nbsp;

### Installing zlib
From the "build-wrf/libraries" directory, type the following commands:
* wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz
* cd zlib-1.2.11
* ./configure --prefix=$DIR/grib2
* make
* make install
* cd ..
* rm zlib-1.2.11.tar.gz
* export LDFLAGS="-L$DIR/grib2/lib -L$DIR/netcdf/lib"
* export CPPFLAGS="-I$DIR/grib2/include -I$DIR/netcdf/lib"
* ![image](https://github.com/user-attachments/assets/ada181cd-b96e-498e-9ad0-c2b472d0979e)  

&nbsp;


### Installing libpng
From the "build-wrf/libraries" directory, type the following commands:
* wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
* tar xzvf libpng-1.2.50.tar.gz
* cd libpng-1.2.50
* ./configure --prefix=$DIR/grib2
* make
* make install
* cd ..
* rm libpng-1.2.50.tar.gz

&nbsp;


### Installing jasper  
From the "build-wrf/libraries" directory, type the following commands:
* wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz
* tar xzvf jasper-1.900.1.tar.gz
* cd jasper-1.900.1
* ./configure --prefix=$DIR/grib2
* make
* make install
* cd ..
* rm jasper-1.900.1.tar.gz

&nbsp;

### Installing hdf5
From the "build-wrf/libraries" directory, type the following commands:
* wget https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_5.tar.gz
* tar xzvf hdf5-1.10.5.tar.gz
* cd hdf5-hdf5-1_10_5
* ./configure --prefix=$DIR/netcdf --with-zlib=$DIR/grib2 --enable-fortran --enable-shared
* make
* make install
* cd ..
* rm hdf5-1.10.5.tar.gz


&nbsp;


# Library Compatibility Test
We've ensured the compilers are compatible, but now we need to ensure that the libraries of Fortran, C, and NetCDF are compatible.  
Again, if you're compiling these on LSU's systems there should be no incompatiblities.  
* In the same "build_wrf/tests" directory the compiler tests were run in, download [THIS](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_NETCDF_MPI_tests.tar) tar file which contains the libraries test files.
* Unpack the tar file with "tar -xf Fortran_C_NETCDF_MPI_tests.tar"
### Test #1
* Type the following commands:
* cp ${NETCDF}/include/netcdf.inc .
* gfortran -c 01_fortran+c+netcdf_f.f
* gcc -c 01_fortran+c+netcdf_c.c
* gfortran 01_fortran+c+netcdf_f.o 01_fortran+c+netcdf_c.o \-L${NETCDF}/lib -lnetcdff -lnetcdf
* ./a.out
* The following should be outputted:
  * "C function called by Fortran
  * Values are xx = 2.00 and ii = 1
  * SUCCESS test 1 fortran + c + netcdf"
### Test #2
* Type the following commands
  * cp ${NETCDF}/include/netcdf.inc .
  * mpif90 -c 02_fortran+c+netcdf+mpi_f.f
  * mpicc -c 02_fortran+c+netcdf+mpi_c.c
  * mpif90 02_fortran+c+netcdf+mpi_f.o \
02_fortran+c+netcdf+mpi_c.o \
     -L${NETCDF}/lib -lnetcdff -lnetcdf  
  * mpirun ./a.out  
* The following should be outputted:
  * C function called by Fortran
  * Values are xx = 2.00 and ii = 1
  * status = 2
  * SUCCESS test 2 fortran + c + netcdf + mpi  


 &nbsp;  

 # Building WRF and WPS
Now we can actually compile WRF and then WPS.  For this tutorial and in general, I use [WRF-4.2.2](https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz) with [WPS-4.2](https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz).  The compilation choices will be chosen with LSU's systems in mind.  
### Building WRF
* From the "build-wrf" directory, download WRF and untar with the below commands:
  * wget https://github.com/wrf-model/WRF/archive/refs/tags/v4.2.2.tar.gz
  * tar xzvf v4.2.2.tar.gz
  * rm v4.2.2.tar.gz
    This should create a directory called "WRF-4.2.2"  
    ![image](https://github.com/user-attachments/assets/11a29fcb-dde3-4c37-905a-378849997422)  
 
    
* Navigate into the "build-wrf/WRF-4.2.2" and create the configure file with:
  * cd WRF-4.2.2
  * ./configure
    * You'll see a large number of options for you to select how to configure WRF based on your system.
    * They correspond to which compiler you are using and whether you want WRF to run serially, Shared-Memory Parallelism, or with Distributed-Memory Parallelism.  More information on these can be found [here](https://forum.mmm.ucar.edu/threads/compiling-options-serial-vs-smpar-vs-dmpar.65/).  
    * Because LSU's systems use a series of clusters and we compiled with gfortran select option 34 by typing "34"
    * type "1" for the "Compile for nesting?" option.  This allows nested simulations.
    * ![image](https://github.com/user-attachments/assets/6ac672f6-c70b-44ab-9d73-add55803f8ed)  
   
  * 







&nbsp;

### Building WPS
  *  wget https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz  
* 
 
  






