# Introduction
This is a written account of my attempt to compile WRF4.2 as of 1/22/2025.  
This follows the official WRF tutorial found [HERE](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php), but also includes photos and any tips or troubles I run into.  
&nbsp;

Important Note: I am compiling this on a system that has all of the necessary libraries such as GNU gcc and foretran already installed.  
&nbsp;

Important Note: The items I tell you to type are in quotes. Don't type the quotes.  They are simply there to help delineate instructions.
For example, if I tell you to type "which gfortran", you type what's between the quotes but not the quotes themselves.  

# Tars
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

# Acquiring System Environment Tests
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

### Conducting System Environment Tests
* There are seven tests that will be run.  Each is a subheading below.
* From your "/work/[your_username]/build-wrf/tests" directory Type:
### Test #1
```
gfortran TEST_1_fortran_only_fixed.f
./a.out
```
* The following should be outputted: "SUCCESS test 1 fortran only fixed format".
### Test #2
```
gfortran TEST_2_fortran_only_free.f90
./a.out
```
* The following should be outputted: "Assume Fortran 2003: has FLUSH, ALLOCATABLE, derived type, and ISO C Binding
SUCCESS test 2 fortran only free format".  
### Test #3
```
gcc TEST_3_c_only.c
./a.out
```
* The Following should be outputted: "SUCCESS test 3 C only".
### Test #4
```
gcc -c -m64 TEST_4_fortran+c_c.c
gfortran -c -m64 TEST_4_fortran+c_f.f90
gfortran -m64 TEST_4_fortran+c_f.o TEST_4_fortran+c_c.o
./a.out
```
* The following should be outputted: "C function called by Fortran
Values are xx = 2.00 and ii = 1
SUCCESS test 4 fortran calling c".
### Test #5
In addition to the mentioned compilers the WRF build system relies on scripts as the user interface which rely on csh, perl, and sh.  
These tests ensure csh, perl, and sh are working properly.  
```
./TEST_csh.csh
```
* The following should be outputted: "SUCCESS csh test".
### Test #6
```
./TEST_perl.pl
```
* The following should be outputted: "SUCCESS perl test".
### Test #7
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

* First you're going to set some variables that the compilation process expects.  Be warned, setting variables from the terminal in this manner does not save them.  When you close your smic/linux terminal, they will disappear and you will need to retype them.  They will be saved if added to your .bashrc file, but that will be handled at the end.
* Within your "/work/[your_username]/build-wrf" directory type:
```
mkdir libraries
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
* tar xzvf zlib-1.2.11.tar.gz
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

### Removing Leap Years from WRF
If you wish to compile your WRF without Leap Days (i.e., skips Feb. 29th every 4 years), follow these steps.  If you want leap-days then you can skip to the "./compile em_real >& log.compile" step
* From the "build-wrf/WRF-4.2.2" directory open the "configure.wrf" file.
* Navigate down to the "Architecture Specific Settings" section.
* To the line "ARCH_LOCAL" add at the end, "-DNO_LEAP_CALENDAR"
* Save and close "configure.wrf"
* ![image](https://github.com/user-attachments/assets/9ddbde93-1be7-490c-9338-e98fb80f2e42)

* This is the end of the Removing Leap Years Section

&nbsp;


Once you've either skipped the leap year removal or completed it, proceed here.

&nbsp;


* Type:
  * ./compile em_real >& log.compile
* The process will probably take some time (maybe 20-30 minutes).
* This tutorial uses the "em_real" "case_name", which is the most common option and what I use as it's designed for real data situations.  Other options can be found in the official WRF tutorial [here](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php).
* The end of the log.compile should look like the picture below if it ran correctly.
* ![image](https://github.com/user-attachments/assets/3eb0f3c2-573d-4a00-8d1c-f628e1f92fa6)
* You can also check that the essential .exe files were properly created with :
  * ls -ls main/*.exe
  * ![image](https://github.com/user-attachments/assets/5c651dc0-ea90-49d8-8c58-2f31f6dd97b7)
  * The numbers circled are the file size in bytes.  They should be around this size (~65MB), but if they are 0 bytes, something has gone wrong in the compilation process and you need to check the log.compile for an error.
 Congrats! You've successfully compiled WRF-4.2.2 and now we only need to worry about WPS.





&nbsp;

### Building WPS
This step will build the WRF-Preprocessing System.  It will be very similar to the Building WRF section.
* From the "build-wrf/libraries" directory, type:
  * wget https://github.com/wrf-model/WPS/archive/refs/tags/v4.2.tar.gz  
  * tar xzvf v4.2.tar.gz
  * rm v4.2.tar.gz
* This will create the "WPS-4.2" directory.
  * ![image](https://github.com/user-attachments/assets/e18e3f4c-68a4-4111-8c94-88be92547b0c)

&nbsp;


*  Navigate into the WPS-4.2 directory with "cd WPS-4.2" and type:
  *  export WRF_DIR=[path to build-wrf]/build-wrf/WRF-4.2.2
  *  ./configure
*  There will be 40 options for compilers to use for WPS.  We want to compile WPS with the same compiler chosen in the Building WRF step.  For myself—because we used gfortran, want the ability to use clusters on LSU systems, and nest simulations—we are choosing the "Linux x86_64, gfortran (dmpar)" option.
*  ![image](https://github.com/user-attachments/assets/9eac0e28-2819-4265-9b9b-3637e58b857f)

### Removing Leap Years from WPS
Similar to WRF, if you're running a similation with a Feb. 29th but your forcing data doesn't account for leap days, WPS will fail to run.  This step tells you how you can prevent WPS from incorporating Feb. 29th.  This step is not necessary and can be skipped if desired.
* After configuring WPS, a "configure.wps" file will be created.
  * Open the "configure.wps"
  * Navigate to the subheading "Architecture Specific Settings" and find the line "CPPFLAGS"
  * At the end of that line, add "-DNO_LEAP_CALENDAR"
  * Save and Close
  * ![image](https://github.com/user-attachments/assets/18a04931-2ad4-4700-ac54-e9a305f7abe7)

 &nbsp;



 &nbsp;


 &nbsp;


 If you completed or skipped the "Removing Leap Years from WPS" section, pick back up here with the compilation!
 * from the "build-wrf/WPS-4.2" type:
   * ./compile >& log.compile
   * ![image](https://github.com/user-attachments/assets/bd74ef03-0ea1-45b2-bc4c-016da6b32421)
 * This will only take a couple minutes to finish.  Once done, 3 executables should appear in the WPS-4.2 directory
   * geogrid.exe
   * ungrib.exe
   * metgrid.exe   
 * The .exe files listed above are symbolic links.  A symbolic link is kind of like a desktop shortcut.  The file itself is not housed in the top-level of the WPS directory, but we've created a shortcut and can manipulate each of those files for ease.
 * To ensure the WPS process ran correctly, make sure each of these is not zero sized by typing the following from the "build-wrf/WPS-4.2" directory:
   * ls -ls geogrid/src/geogrid.exe
   * ls -ls metgrid/src/metgrid.exe
   * ls -ls ungrib/src/ungrib.exe

 * ![image](https://github.com/user-attachments/assets/b4243502-5cf8-4b0c-9de7-12ef2099c3bc)

   &nbsp;

   &nbsp;

   &nbsp;

   # Static Geography Data
The last thing that needs to be done is set up the "static geography data."  These are variables such as soiltype or albedo or land useage that does not change often and so is considered "static" data that is necessary for WRF to run.  
The link to the download page is [HERE](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html). 

&nbsp;

Important Note: In my experience, geogrid.exe often requires a few more geog files than are actually prvided in the below tar.  If you encounter an error running geogrid.exe related to a non-existing file in the geog directory, go to the above webpage and manually download and add it to the geog directory.  There is also a step-by-step guide on how to do this on the "WRF Trouble Shooting and Tips" page of this github.  

&nbsp;

* Navigate to the "build-wrf" directory ("cd .." if you just compiled WPS) and type:
  * wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
  * tar -xf geog_high_res_mandatory.tar.gz
    * Important Note: this will be about 30GB of data
* When you use the WPS process, in the namelist.wps be sure to set the "geog_data_path" to this directory with:
  *  geog_data_path = [path_to_build-wrf]/build-wrf/WPS_GEOG
  *  ("WPS_GEOG" is a newer naming convention, which is why mine is called "geog" in the picture below)
  *  ![image](https://github.com/user-attachments/assets/24feb2d9-2384-468d-8aa1-2f8a5650ed36)
 

&nbsp;

# Adding Environmental Variables to .bashrc
This section takes most of those environmental variables set at the start of the tutorial and adds them to your .bashrc file.  This is important because otherwise when you close the terminal you'll lose the environmental variables you set, some of which are essential to run WRF.  

*Open the .bashrc file with either of the below commands:
  *  vi ~/.bashrc
  *  nano ~/.bashrc
*  Make sure the below environmental variables  are added to the file
  * export WRF_DIR=/work/cjoh513/build-wrf/WRF-4.2.2
  * export WRF_CHEM=1
  * export WRF_KPP=0
  * export WRFIO_NCD_LARGE_FILE_SUPPORT=1
  * export DIR=/work/cjoh513/build-wrf/libraries
  * export PATH=$DIR/netcdf/bin:$DIR/mpich/bin:$PATH
  * export NETCDF=$DIR/netcdf
  * export JASPERLIB=$DIR/grib2/lib
  * export JASPERINC=$DIR/grib2/include
  * export CC=gcc
  * export CXX=g++
  * export FC=gfortran
  * export FCFLAGS=-m64
  * export F77=gfortran
  * export FFLAGS=-m64
* Here is an example of what mine looks like, but there are a few more variables added than strictly for this tutorial.  
* ![image](https://github.com/user-attachments/assets/472643fb-5907-4670-934e-331637da16e7)  




Congratulations!!!  
The process may have been arduous, but you've successfully installed libraries and compiled WRF/WPS.  





  






